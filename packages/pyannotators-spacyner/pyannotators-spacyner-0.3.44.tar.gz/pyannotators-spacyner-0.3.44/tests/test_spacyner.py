import gzip
import json
import string
import xml.etree.ElementTree as ET
from collections import defaultdict, Counter, namedtuple, Iterable
from functools import lru_cache
from itertools import product, chain, combinations, islice
from pathlib import Path
from typing import List

import mongoquery as mongoquery
import pandas as pd
import pytest as pytest
import requests as requests
from blingfire import text_to_sentences_and_offsets
from collections_extended import RangeMap
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from metapub import PubMedArticle
from pyannotators_spacyner.spacyner import SpacyNERAnnotator, SpacyNERParameters, get_nlp
from pybel.parser import BELParser
from pymultirole_plugins.v1.schema import Document, DocumentList, Sentence, Annotation
from ratelimit import sleep_and_retry, limits
from requests_cache import CachedSession
from tqdm import tqdm


def test_spacyner():
    model = SpacyNERAnnotator.get_model()
    model_class = model.construct().__class__
    assert model_class == SpacyNERParameters
    annotator = SpacyNERAnnotator()
    parameters = SpacyNERParameters()
    docs: List[Document] = annotator.annotate([Document(
        text="Paris is the capital of France and Emmanuel Macron is the president of the French Republic.",
        metadata=parameters.dict())], parameters)
    doc0 = docs[0]
    assert len(doc0.annotations) == 4
    paris = doc0.annotations[0]
    france = doc0.annotations[1]
    macron = doc0.annotations[2]
    republic = doc0.annotations[3]
    assert paris.label == 'GPE'
    assert france.label == 'GPE'
    assert macron.label == 'PERSON'
    assert republic.label == 'GPE'


def test_scispacyner():
    model = SpacyNERAnnotator.get_model()
    model_class = model.construct().__class__
    assert model_class == SpacyNERParameters
    annotator = SpacyNERAnnotator()
    parameters = SpacyNERParameters(model='en_core_sci_sm')
    docs: List[Document] = annotator.annotate([Document(
        text="Myeloid derived suppressor cells (MDSC) are immature myeloid cells with immunosuppressive activity.\nThey accumulate in tumor-bearing mice and humans with different types of cancer, including hepatocellular carcinoma (HCC).",
        metadata=parameters.dict())], parameters)
    doc0 = docs[0]
    assert len(doc0.annotations) == 12


def test_cached_nlp():
    parameters1 = SpacyNERParameters()
    nlp1, linker1 = get_nlp(parameters1.model)
    parameters2 = SpacyNERParameters()
    nlp2, linker2 = get_nlp(parameters2.model)
    assert id(nlp1) == id(nlp2)


def to_camel_case(s):
    return s[0].lower() + string.capwords(s, sep='_').replace('_', '')[1:] if s else s


@pytest.mark.skip(reason="Not a test")
def test_scai_parse():
    testdir = Path(__file__).parent / 'data'
    excel_file = testdir / "all_bel_relations.xlsx"
    bel_df = pd.read_excel(excel_file).fillna(value="")
    docs = {}
    docids = Counter()
    for index, row in bel_df.iterrows():
        subject = row['Subject']
        relation = row['Relation']
        object = row['Object']
        docid = str(row['PubMedID'])
        sentence = row['EvidenceSentence']
        title = row['PublicationTitle']
        sent = subject + " " + to_camel_case(relation) + " " + object
        docids.update([docid])
        docinc = docids[docid]
        doc = docs.get((docid, sentence))
        if doc is None:
            doc = Document(identifier=f"{docid}-{docinc}", title=title, text=sentence,
                           sentences=[Sentence(start=0, end=len(sentence))], metadata={"bel_sentences": [sent]})
            docs[(docid, sentence)] = doc
        else:
            doc.metadata['bel_sentences'].append(sent)
        # parsed_sent = pybel.parse(sent)
    dl = DocumentList(__root__=list(docs.values()))
    json_file = testdir / "all_bell_relations.json"
    with json_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


@pytest.mark.skip(reason="Not a test")
def test_scai():
    annotator = SpacyNERAnnotator()
    parameters = SpacyNERParameters(model='en_core_sci_sm', scispacy_linker='umls',
                                    types_filter=['T028', 'T116', 'T123', 'T126', 'T043', 'T047', 'T121', 'T109',
                                                  'T026', 'T025', 'T129', 'T192', 'T044', 'T048', 'T043', 'T131',
                                                  'T125', 'T043', 'T130', 'T196', 'T005', 'T008', 'T010', 'T012',
                                                  'T013', 'T014', 'T015', 'T016', 'T017', 'T018', 'T021', 'T022',
                                                  'T023', 'T024', 'T025', 'T026'
                                                  ])
    parameters = SpacyNERParameters(model='en_core_sci_sm', scispacy_linker='umls')
    testdir = Path(__file__).parent / 'data'
    # json_file = testdir / "scai_test_sherpa.json"
    json_file = testdir / "all_bell_relations.json"
    with json_file.open("r") as fin:
        docs = json.load(fin)
    docs = [Document(**doc) for doc in docs]
    docs = annotator.annotate(docs, parameters)
    json_file = testdir / f"all_bell_relations_annotated_{parameters.scispacy_linker.value}.json"
    # json_file = testdir / f"scai_test_sherpa_{parameters.scispacy_linker.value}.json"
    dl = DocumentList(__root__=docs)
    with json_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


def find_in_forms(el, forms):
    for k in el:
        if 'name' in el[k]:
            name = el[k]['name']
            if name.lower() in forms:
                return k
    return None


def fuzzy_find_in_annot(el, a, threshold=80):
    forms = a.properties.get('forms', [])
    for k in el:
        if isinstance(el[k], dict):
            if 'name' in el[k]:
                name = el[k]['name']
                extracted = process.extractOne(name.lower(), forms, scorer=fuzz.token_sort_ratio)
                if extracted and extracted[1] > threshold:
                    copy_el = {k1: v1 for k1, v1 in el.items() if k1 in ['function', k, 'kind']}
                    return copy_el
                else:
                    pass
        elif isinstance(el[k], list):
            for subel in el[k]:
                ret = fuzzy_find_in_annot(subel, a, threshold)
                if ret is not None:
                    return ret
    return None


# Amino Acid	1-Letter Code	3-Letter Code
AMINOS = {
    "A": "Alanine", "Ala": "Alanine",
    "R": "Arginine", "Arg": "Arginine",
    "N": "Asparagine", "Asn": "Asparagine",
    "D": "Aspartic Acid", "Asp": "Aspartic Acid",
    "C": "Cysteine", "Cys": "Cysteine",
    "E": "Glutamic Acid", "Glu": "Glutamic Acid",
    "Q": "Glutamine", "Gln": "Glutamine",
    "G": "Glycine", "Gly": "Glycine",
    "H": "Histidine", "His": "Histidine",
    "I": "Isoleucine", "Ile": "Isoleucine",
    "L": "Leucine", "Leu": "Leucine",
    "K": "Lysine", "Lys": "Lysine",
    "M": "Methionine", "Met": "Methionine",
    "F": "Phenylalanine", "Phe": "Phenylalanine",
    "P": "Proline", "Pro": "Proline",
    "S": "Serine", "Ser": "Serine",
    "T": "Threonine", "Thr": "Threonine",
    "W": "Tryptophan", "Trp": "Tryptophan",
    "Y": "Tyrosine", "Tyr": "Tyrosine",
    "V": "Valine", "Val": "Valine"
}

PMod = namedtuple('PMod', ['prot', 'type', 'at'])


def extract_pmods(el, pmods=[]):
    if 'function' in el:
        if el['function'] == 'Protein':
            pmod = PMod(None, None, None)
            copy_el = {k1: v1 for k1, v1 in el.items() if k1 in ['function', 'concept']}
            pmod = pmod._replace(prot=copy_el)
            if 'variants' in el:
                for variant in el['variants']:
                    if variant['kind'] == 'pmod':
                        copy_el = {k1: v1 for k1, v1 in variant.items() if k1 in ['function', 'concept']}
                        copy_el["function"] = "ModType"
                        pmod = pmod._replace(type=copy_el)
                        if 'code' in variant:
                            if variant['code'] in AMINOS:
                                pmod_at = AMINOS[variant['code']]
                                if 'pos' in variant:
                                    pmod_at += f" {variant['pos']}"
                                pmod = pmod._replace(at={
                                    "function": "AminoAcid",
                                    "concept": {
                                        "name": pmod_at
                                    }
                                })
            if pmod.prot is not None and pmod.type is not None:
                pmods.append(pmod)
            # else:
            #     print(f"Incomplete pmod {pmod} in {el}")
        elif el['function'] == 'Complex' and 'members' in el:
            for member in el['members']:
                extract_pmods(member, pmods)


def add2rows(el, rows):
    row = {}
    for k in el:
        if k == "function":
            row[k] = el[k]
        elif 'namespace' in el[k]:
            row[k] = el[k]['namespace']
    rows.append(row)


greek_alphabet = 'ΑαΒβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσςΤτΥυΦφΧχΨψΩω'
latin_alphabet = 'AaBbGgDdEeZzHhJjIiKkLlMmNnXxOoPpRrSssTtUuFfQqYyWw'
greek2latin = str.maketrans(greek_alphabet, latin_alphabet)
greek2english_alphabet = {
    u'\u0391': 'Alpha',
    u'\u0392': 'Beta',
    u'\u0393': 'Gamma',
    u'\u0394': 'Delta',
    u'\u0395': 'Epsilon',
    u'\u0396': 'Zeta',
    u'\u0397': 'Eta',
    u'\u0398': 'Theta',
    u'\u0399': 'Iota',
    u'\u039A': 'Kappa',
    u'\u039B': 'Lamda',
    u'\u039C': 'Mu',
    u'\u039D': 'Nu',
    u'\u039E': 'Xi',
    u'\u039F': 'Omicron',
    u'\u03A0': 'Pi',
    u'\u03A1': 'Rho',
    u'\u03A3': 'Sigma',
    u'\u03A4': 'Tau',
    u'\u03A5': 'Upsilon',
    u'\u03A6': 'Phi',
    u'\u03A7': 'Chi',
    u'\u03A8': 'Psi',
    u'\u03A9': 'Omega',
    u'\u03B1': 'alpha',
    u'\u03B2': 'beta',
    u'\u03B3': 'gamma',
    u'\u03B4': 'delta',
    u'\u03B5': 'epsilon',
    u'\u03B6': 'zeta',
    u'\u03B7': 'eta',
    u'\u03B8': 'theta',
    u'\u03B9': 'iota',
    u'\u03BA': 'kappa',
    u'\u03BB': 'lamda',
    u'\u03BC': 'mu',
    u'\u03BD': 'nu',
    u'\u03BE': 'xi',
    u'\u03BF': 'omicron',
    u'\u03C0': 'pi',
    u'\u03C1': 'rho',
    u'\u03C3': 'sigma',
    u'\u03C4': 'tau',
    u'\u03C5': 'upsilon',
    u'\u03C6': 'phi',
    u'\u03C7': 'chi',
    u'\u03C8': 'psi',
    u'\u03C9': 'omega',
}
greek2english = str.maketrans(greek2english_alphabet)


@pytest.mark.skip(reason="Not a test")
def test_scai_train():
    testdir = Path(__file__).parent / 'data'
    json_file = testdir / "all_bell_relations_matched_umls.json"
    with json_file.open("r") as fin:
        jdocs = json.load(fin)
    docs = []
    for jdoc in jdocs:
        doc = Document(**jdoc)
        new_annotations = []
        if doc.identifier not in ['19885299-118'] and doc.metadata['corpus'] == 'train':
            # for s in doc.sentences:
            #     stext = doc.text[s.start:s.end]
            for a in doc.annotations:
                a.properties = None
                a.terms = None
                new_annotations.append(a)
            doc.annotations = new_annotations
            docs.append(doc)
    json_file = testdir / "all_bell_relations_training_umls.json"
    dl = DocumentList(__root__=docs)
    with json_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


def closest_entities(list1, list2):
    min_gap = 2 ** 31
    min_span = (0, 0)
    for a1, a2 in product(list1, list2):
        span = (min(a1.start, a2.start), max(a1.end, a2.end))
        gap = (span[1] - span[0]) - (a1.end - a1.start) - (a2.end - a2.start)
        if gap <= min_gap and (span[1] - span[0]) > (min_span[1] - min_span[0]):
            min_span = span
    return span


@pytest.mark.skip(reason="Not a test")
def test_scai_pubmed():
    TUIs2Class = {
        'T109': 'Abundance',
        'T121': 'Abundance',
        'T123': 'Abundance',
        'T005': 'Abundance',
        'T028': 'Protein',
        'T116': 'Protein',
        'T126': 'Protein',
        'T043': 'BiologicalProcess',
        'T047': 'Pathology',
        'T048': 'Pathology',
        'T008': 'Specie',
        'T010': 'Specie',
        'T012': 'Specie',
        'T013': 'Specie',
        'T014': 'Specie',
        'T015': 'Specie',
        'T016': 'Specie',
        'T017': 'Location',
        'T018': 'Location',
        'T021': 'Location',
        'T022': 'Location',
        'T023': 'Location',
        'T024': 'Location',
        'T025': 'Location',
        'T026': 'Location'
    }
    killCUIs = [
        "C0017337",
        "C0171406",
        "C0597357",
        "C4318409",
        "C0012634",
        "C0305060",
        "C1824234"
    ]

    def tui2class(a):
        classes = set()
        for t in a.terms[0].properties['types']:
            if t in TUIs2Class:
                classes.add(TUIs2Class[t])
        return list(classes)

    def killtui2(a):
        return a.terms[0].identifier in killCUIs

    annotator = SpacyNERAnnotator()
    parameters = SpacyNERParameters(model='en_core_sci_sm', scispacy_linker='umls',
                                    types_filter=list(TUIs2Class.keys()))
    testdir = Path('/media/olivier/DATA/corpora/SCAI/MedlineCorpus-Schizophrenia-BipolarDisorder-20210907')
    for pubmed_gz in tqdm(testdir.glob('*.xml.gz')):
        with gzip.open(pubmed_gz) as fin:
            tree = ET.parse(fin)
            docs = []
            for article in tree.iter('PubmedArticle'):
                art_xml = ET.tostring(article[0])
                art = PubMedArticle(art_xml)
                if art.title is not None or art.abstract is not None:
                    art.title = art.title or ''
                    art.abstract = art.abstract or ''
                    doc = Document(identifier=str(art.pmid), title=art.title, text=art.title + "\n\n" + art.abstract,
                                   metadata={'journal': art.journal},
                                   sentences=[])
                    result = text_to_sentences_and_offsets(doc.text)
                    if result:
                        for start, end in result[1]:
                            doc.sentences.append(Sentence(start=start, end=end))
                            docs.append(doc)
            docs = annotator.annotate(docs, parameters)
            output_sents = []
            for document in docs:
                sent_map = RangeMap()
                for isent, sent in enumerate(document.sentences):
                    sent_map[sent.start:sent.end] = []
                for a in document.annotations:
                    if not killtui2(a):
                        alist = sent_map[a.start]
                        alist.append(a)
                for isent, (sstart, sstop, slist) in enumerate(sent_map.ranges()):
                    sent = document.sentences[isent]
                    if len(slist) > 1:
                        stext = document.text[sent.start:sent.end]
                        ents = []
                        output_sent = {
                            'PubMedID': document.identifier,
                            'PublicationTitle': document.title,
                            'Journal': document.metadata['journal'],
                            'EvidenceSentence': stext,
                            'Entities': ents
                        }
                        for a in slist:
                            classes = tui2class(a)
                            for c in classes:
                                ents.append(
                                    {
                                        'namespace': 'UMLS',
                                        'name': a.terms[0].preferredForm,
                                        'class': c,
                                        'identifier': a.terms[0].identifier,
                                        'start': a.start - sstart,
                                        'end': a.end - sstart
                                    }
                                )
                        real_classes = {e['identifier'] for e in ents if e['class'] not in ['Location', 'Specie']}
                        if len(real_classes) > 1:
                            output_sents.append(output_sent)
        json_file = pubmed_gz.with_suffix(".json")
        with json_file.open("w") as fout:
            json.dump(output_sents, fout, indent=2)


# SHERPA_SERVER = "https://sherpa-sandbox.kairntech.com/"
SHERPA_SERVER = "http://localhost:7070"


def get_token(server=SHERPA_SERVER, user="oterrier", password="ote123;"):
    url = server + "/api/auth/login"
    auth = {"email": user, "password": password}
    try:
        response = requests.post(url, json=auth,
                                 headers={'Content-Type': "application/json", 'Accept': "application/json"},
                                 verify=False)
        json_response = json.loads(response.text)
    except Exception as ex:
        print("Error connecting to Sherpa server %s: %s" % (server, ex))
        return
    if 'access_token' in json_response:
        token = json_response['access_token']
        return token
    else:
        return


def find_pmod_type(text):
    atext = text.lower()
    if 'phospho' in atext:
        return 'Ph'
    elif 'acety' in atext:
        return 'Ac'
    elif 'oxi' in atext or 'oxy' in atext:
        return 'Ox'
    elif 'palm' in atext:
        return 'Palm'
    elif 'nitro' in atext:
        return 'NO'
    elif 'nedd' in atext:
        return 'Nedd'
    elif 'nglyco' in atext or ('N' in text and 'glyco' in atext):
        return 'NGlyco'
    elif 'oglyco' in atext or ('O' in text and 'glyco' in atext):
        return 'OGlyco'
    elif 'myr' in atext:
        return 'Myr'
    elif 'monomethyl' in atext or 'mono-methyl' in atext:
        return 'Me1'
    elif 'dimethyl' in atext or 'di-methyl' in atext:
        return 'Me2'
    elif 'trimethyl' in atext or 'tri-methyl' in atext:
        return 'Me3'
    elif 'methyl' in atext:
        return 'Me'
    elif 'hydroxy' in atext:
        return 'Hy'
    elif 'glyco' in atext:
        return 'Glyco'
    elif 'gerger' in atext:
        return 'Gerger'
    elif 'farn' in atext:
        return 'Farn'
    elif 'adp' in atext and ('rib' in atext or 'ryb' in atext):
        return 'ADPRib'
    elif 'sulf' in atext or 'sulph' in atext:
        return 'Sulf'
    elif 'sumo' in atext:
        return 'Sumo'
    elif 'ubiqu' in atext and 'mono' in atext:
        return 'UbMono'
    elif 'ubiqu' in atext and 'poly' in atext:
        return 'UbPoly'
    elif 'ubiqu' in atext:
        return 'Ub'
    return None


hgnc_url = 'http://rest.genenames.org'
hsession = CachedSession(cache_name='hgnc_cache', backend='sqlite')
hsession.headers.update({'Content-Type': "application/json", 'Accept': "application/json"})
hsession.verify = False


@sleep_and_retry
@limits(calls=10, period=1)
def hgnc_search(query):
    try:
        return hsession.get(f'{hgnc_url}/search/"{query}"')
    except Exception as e:
        print(e)
    return None


@lru_cache(maxsize=1000)
def fuzzy_search_gene(names):
    queries = set()
    for name in names:
        queries.add(name)
        if 'protein' in name:
            queries.add(name.replace('protein', ''))
        gname = name.translate(greek2latin)
        _name = name.replace('-', '')
        if name != _name:
            queries.add(_name)
        if name != gname:
            queries.add(gname)
            ename = name.translate(greek2english)
            queries.add(ename)
            if name != _name:
                queries.add(gname.replace('-', ''))
                queries.add(ename.replace('-', ''))
    genes = [search_gene(q) for q in queries]
    gene = max(genes, key=lambda g: g[1])
    return gene[0]


@lru_cache(maxsize=10000)
def search_gene(query):
    resp = hgnc_search(query)
    if resp and resp.ok:
        r = resp.json()['response']
        maxScore = r['maxScore']
        candidates = [d for d in r['docs'] if d['score'] >= maxScore]
        forms = []
        symbols = []
        gmap = {}
        for c in candidates:
            genes = fetch_gene(c['symbol'])
            for g in genes:
                gmap[g['symbol']] = g
                symbols.append(c['symbol'])
                forms.append(g['symbol'])
                symbols.append(c['symbol'])
                forms.append(g['name'])
                for n in chain(g.get('prev_name', []), g.get('alias_symbol', []), g.get('alias_name', [])):
                    symbols.append(c['symbol'])
                    forms.append(n)
        extracted = process.extractOne(query.lower(), forms, scorer=fuzz.token_sort_ratio)
        if extracted and extracted[1] > 85:
            index = forms.index(extracted[0])
            symbol = symbols[index]
            gene = gmap[symbol]
            return gene, extracted[1]
    return None, 0


@sleep_and_retry
@limits(calls=10, period=1)
def fetch_gene(query):
    try:
        resp = hsession.get(f'{hgnc_url}/fetch/symbol/"{query}"')
        if resp.ok:
            r = resp.json()['response']
            candidates = r['docs']
            return candidates
    except Exception as e:
        print(e)
    return []


def annotate_with_pmod(doc: Document, token, server=SHERPA_SERVER, project="scai_pmod", annotator="crfsuite"):
    annotate_url = server + ('/api/projects/%s/annotators/%s/_annotate_document' % (project, annotator))
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': "application/json", 'Accept': "application/json"}
    ddoc = {k: v for k, v in doc.dict().items() if k in ['text', 'title', 'sentences', 'identifier']}
    for sent in ddoc['sentences']:
        if 'metadata' in sent:
            del sent['metadata']
        if 'categories' in sent:
            del sent['categories']
    r = requests.post(annotate_url, json=ddoc, headers=headers, verify=False, timeout=1000)
    if r.ok:
        annotated = Document(**r.json())
        for a in annotated.annotations:
            if a.labelName == 'modtype':
                a.properties = {}
                a.properties['name'] = find_pmod_type(a.text)
            elif a.labelName == 'protein':
                atext = annotated.text[a.start:a.end]
                gene = fuzzy_search_gene((atext,))
                if gene is None:
                    print(f"Not found in HGNC: {atext}")
                else:
                    a.properties = {}
                    a.properties['namespace'] = 'HGNC'
                    a.properties['name'] = gene['symbol']
                    a.properties['identifier'] = (gene['hgnc_id'].split(':'))[-1]
                pass
        return annotated
    return None


def annotate_with_ef(doc):
    APP_EF_URI = "https://sherpa-entityfishing.kairntech.com"
    dsession = requests.Session()
    dsession.headers.update({'Content-Type': "application/json", 'Accept': "application/json"})
    dsession.verify = False
    ksession = CachedSession(cache_name='ef_cache', backend='sqlite')
    ksession.headers.update({'Content-Type': "application/json", 'Accept': "application/json"})
    ksession.verify = False
    disamb_url = APP_EF_URI + '/service/disambiguate'
    kb_url = APP_EF_URI + '/service/kb/concept/'

    # import pyhgnc
    # pyhgnc.manager.database.update()

    def find_property(concept, pname):
        stmts = []
        for s in concept.get('statements', []):
            if s.get('propertyName', None) == pname or s.get('propertyId', None) == pname:
                stmts.append(s)
        return stmts

    kill_list = [
        "increase",
        "increases",
        "increased",
        "decrease",
        "decreases",
        "decreased",
        "induced",
        "induce",
        "induces",
        "largest extant",
        "antibody",
        "antibodies",
        "receptor",
        "receptors",
        "alleles",
        "allele",
        "enzyme",
        "enzymes",
        "multiple genes",
        "genes",
        "gene",
        "proteins",
        "protein",
        "conditions",
        "condition",
        "syndrome",
        "syndromes",
        "diseases",
        "disease",
        "drug",
        "drugs",
        "treat",
        "treats",
        "treated",
        "expressed",
        "express",
        "expresses",
        "expression"
    ]
    MAPPING = {
        "Protein":
            {
                "statements":
                    {
                        "$elemMatch":
                            {
                                "$or":
                                    [
                                        {
                                            "$and":
                                                [
                                                    {
                                                        "propertyId":
                                                            {
                                                                "$in":
                                                                    [
                                                                        "P31",
                                                                        "P279"
                                                                    ]
                                                            }
                                                    },
                                                    {
                                                        "value":
                                                            {
                                                                "$in":
                                                                    [
                                                                        "Q7187",
                                                                        "Q410221",
                                                                        "Q67015883",
                                                                        "Q8054",
                                                                        "Q407384",
                                                                        "Q78155096",
                                                                        "Q84467700"
                                                                    ]
                                                            }
                                                    }
                                                ]
                                        },
                                        {
                                            "propertyId":
                                                {
                                                    "$in":
                                                        [
                                                            "P351",
                                                            "P594"
                                                        ]
                                                }
                                        },
                                        {
                                            "$and":
                                                [
                                                    {
                                                        "propertyId": "P672"
                                                    },
                                                    {
                                                        "value":
                                                            {
                                                                "$regex": "G05[.]360.+"
                                                            }
                                                    }
                                                ]
                                        }
                                    ]
                            }
                    }
            },
        "Abundance":
            {
                "statements":
                    {
                        "$elemMatch":
                            {
                                "$or":
                                    [
                                        {
                                            "propertyId": "P31",
                                            "value": "Q12140"
                                        },
                                        {
                                            "propertyId": "P279",
                                            "value":
                                                {
                                                    "$in":
                                                        [
                                                            "Q12140",
                                                            "Q179661"
                                                        ]
                                                }
                                        },
                                        {
                                            "propertyId": "P683"
                                        }
                                    ]
                            }
                    }
            },
        "Pathology":
            {
                "statements":
                    {
                        "$elemMatch":
                            {
                                "$or":
                                    [
                                        {
                                            "$and":
                                                [
                                                    {
                                                        "propertyId": "P31"
                                                    },
                                                    {
                                                        "value":
                                                            {
                                                                "$in":
                                                                    [
                                                                        "Q12136",
                                                                        "Q929833",
                                                                        "Q12135"
                                                                    ]
                                                            }
                                                    }
                                                ]
                                        },
                                        {
                                            "propertyId": "P699"
                                        },
                                        {
                                            "$and":
                                                [
                                                    {
                                                        "propertyId": "P672"
                                                    },
                                                    {
                                                        "value":
                                                            {
                                                                "$regex": "C.+"
                                                            }
                                                    }
                                                ]
                                        }
                                    ]
                            }
                    }
            },
        "BiologicalProcess":
            {
                "statements":
                    {
                        "$elemMatch":
                            {
                                "$or":
                                    [
                                        {
                                            "$and":
                                                [
                                                    {
                                                        "propertyId":
                                                            {
                                                                "$in":
                                                                    [
                                                                        "P31",
                                                                        "P279"
                                                                    ]
                                                            }
                                                    },
                                                    {
                                                        "value":
                                                            {
                                                                "$in":
                                                                    [
                                                                        "Q2996394",
                                                                        "Q14873025"
                                                                    ]
                                                            }
                                                    }
                                                ]
                                        },
                                        # {
                                        #     "propertyId": "P686"
                                        # },
                                        {
                                            "$and":
                                                [
                                                    {
                                                        "propertyId": "P672"
                                                    },
                                                    {
                                                        "value":
                                                            {
                                                                "$regex": "G.+"
                                                            }
                                                    }
                                                ]
                                        }
                                    ]
                            }
                    }
            },
        "Specie":
            {
                "statements":
                    {
                        "$elemMatch":
                            {
                                "$and":
                                    [
                                        {
                                            "propertyId":
                                                {
                                                    "$in":
                                                        [
                                                            "P31",
                                                            "P279"
                                                        ]
                                                }
                                        },
                                        {
                                            "value":
                                                {
                                                    "$in":
                                                        [
                                                            "Q55983715",
                                                            "Q16521",
                                                            "Q5532935"
                                                        ]
                                                }
                                        }
                                    ]
                            }
                    }
            }
    }

    def get_kb_concept(lang, qid):
        resp = ksession.get(kb_url + qid, params={'lang': lang})
        if resp.ok:
            return resp.json()
        else:
            return {}

    @sleep_and_retry
    @limits(calls=10, period=1)
    def disamb_query(text, lang, minSelectorScore, entities=None, sentences=None, segment=False):
        disamb_query = {
            "text": text.replace('\r\n', ' \n'),
            "entities": entities,
            "sentences": sentences,
            "language": {"lang": lang},
            "mentions": ["wikipedia"],
            "nbest": False,
            "sentence": segment,
            "customisation": "generic",
            "minSelectorScore": minSelectorScore
        }
        try:
            resp = dsession.post(disamb_url, json=disamb_query, timeout=(30, 300))
            if resp.ok:
                return resp.json()
        except Exception as e:
            print(e)
        return {}

    sents = [{"offsetStart": s.start, "offsetEnd": s.end} for s in
             doc.sentences] if doc.sentences else []
    doc.annotations = doc.annotations or []
    result = disamb_query(doc.text, "en", 0.2, None, sents)
    entities = []
    if 'entities' in result:
        for entity in result['entities']:
            if 'wikidataId' in entity:
                etext = doc.text[entity['offsetStart']:entity['offsetEnd']]
                if etext.lower() not in kill_list:
                    entities.append(entity)
    qids = {entity['wikidataId'] for entity in entities}
    concepts = {}
    for qid in qids:
        concept = get_kb_concept("en", qid)
        concepts[qid] = concept
    mapped_concepts = {}
    for key, condition in MAPPING.items():
        query = mongoquery.Query(condition)
        filtered = filter(lambda elem: query.match(elem[1]), concepts.items())
        for f in filtered:
            if f[0] not in mapped_concepts:
                mapped_concepts[f[0]] = key
    for entity in entities:
        props = {}
        qid = entity['wikidataId']
        label = mapped_concepts.get(qid, 'Other')
        concept = concepts[qid]
        prefLabel = concept.get('preferredTerm', concept.get('rawName', None))
        etext = doc.text[entity['offsetStart']:entity['offsetEnd']]
        if prefLabel:
            props['name'] = prefLabel
        if label == 'Abundance':
            vals = find_property(concept, 'ChEBI ID')
            if vals:
                props['namespace'] = 'CHEBI'
                props['identifier'] = str(vals[0]['value'])
        elif label == 'Protein':
            valnames = find_property(concept, 'HGNC gene symbol')
            valids = find_property(concept, 'HGNC ID')
            if valnames or valids:
                props['namespace'] = 'HGNC'
                if valnames:
                    props['name'] = str(valnames[0]['value'])
                if valids:
                    props['identifier'] = str(valids[0]['value'])
            else:
                print(f"No HGNC in wikidata: {etext} - {prefLabel}")
                gnames = [etext]
                if prefLabel:
                    gnames.append(prefLabel)
                gene = fuzzy_search_gene(tuple(gnames))
                if gene is None:
                    print(f"Not found in HGNC: {etext} - {prefLabel}")
                    label = 'Other'
                else:
                    label = 'Protein'
                    props['namespace'] = 'HGNC'
                    props['name'] = gene['symbol']
                    props['identifier'] = (gene['hgnc_id'].split(':'))[-1]
        elif label == 'Pathology':
            valids = find_property(concept, 'P486')
            valdoids = find_property(concept, 'P699')
            if valids:
                props['namespace'] = 'MESHD'
                props['identifier'] = str(valids[0]['value'])
            elif valdoids:
                props['namespace'] = 'DO'
                props['identifier'] = (str(valdoids[0]['value']).split(':'))[-1]
        elif label == 'BiologicalProcess':
            valgoids = find_property(concept, 'P686')
            valids = find_property(concept, 'P486')
            if valgoids:
                props['namespace'] = 'GOBP'
                props['identifier'] = str(valgoids[0]['value'])
            elif valids:
                props['namespace'] = 'MESHPP'
                props['identifier'] = str(valids[0]['value'])
        elif label == 'Location':
            valids = find_property(concept, 'P486')
            if valids:
                props['namespace'] = 'MESHA'
                props['identifier'] = str(valids[0]['value'])
        elif label == 'Specie':
            valids = find_property(concept, 'P685')
            valnames = find_property(concept, 'P225')
            if valnames:
                props['name'] = str(valnames[0]['value'])
            if valids:
                props['namespace'] = 'NCBI'
                props['identifier'] = str(valids[0]['value'])
        if len(props) == 0:
            pass
        doc.annotations.append(
            Annotation(start=entity['offsetStart'], end=entity['offsetEnd'], label=label,
                       labelName=label.lower(), text=etext,
                       score=entity.get('confidence_score', 1.0),
                       properties=props))
    return doc


@pytest.mark.skip(reason="Not a test")
def test_scai_ef():
    testdir = Path('/media/olivier/DATA/corpora/SCAI/MedlineCorpus-Schizophrenia-BipolarDisorder-20210907')
    token = get_token()
    for pubmed_gz in tqdm(testdir.glob('*.xml.gz')):
        with gzip.open(pubmed_gz) as fin:
            tree = ET.parse(fin)
            docs = []
            for article in tree.iter('PubmedArticle'):
                art_xml = ET.tostring(article[0])
                art = PubMedArticle(art_xml)
                if art.title is not None or art.abstract is not None:
                    art.title = art.title or ''
                    art.abstract = art.abstract or ''
                    doc = Document(identifier=str(art.pmid), title=art.title, text=art.title + "\n\n" + art.abstract,
                                   metadata={'journal': art.journal},
                                   annotations=[],
                                   sentences=[])
                    result = text_to_sentences_and_offsets(doc.text)
                    if result:
                        for start, end in result[1]:
                            doc.sentences.append(Sentence(start=start, end=end))

                    annotated = annotate_with_ef(doc)
                    pmod_doc = annotate_with_pmod(doc, token)
                    if pmod_doc and pmod_doc.annotations:
                        annotated.annotations.extend(pmod_doc.annotations)
                        annotated.annotations = filter_annotations(annotated)
                    docs.append(annotated)

            output_sents = []
            for document in docs:
                sent_map = RangeMap()
                for isent, sent in enumerate(document.sentences):
                    sent_map[sent.start:sent.end] = []
                for a in document.annotations:
                    if a.label != 'Other':
                        alist = sent_map[a.start]
                        alist.append(a)
                for isent, (sstart, sstop, slist) in enumerate(sent_map.ranges()):
                    sent = document.sentences[isent]
                    if len(slist) > 1:
                        stext = document.text[sent.start:sent.end]
                        ents = []
                        output_sent = {
                            'PubMedID': document.identifier,
                            'PublicationTitle': document.title,
                            'Journal': document.metadata['journal'],
                            'EvidenceSentence': stext,
                            'Entities': ents
                        }
                        for a in slist:
                            ent = {
                                'class': a.label,
                                'start': a.start - sstart,
                                'end': a.end - sstart,
                                'name': document.text[a.start:a.end]
                            }
                            if a.properties:
                                if 'identifier' in a.properties:
                                    ent['identifier'] = a.properties['identifier']
                                if 'namespace' in a.properties:
                                    ent['namespace'] = a.properties['namespace']
                                if 'name' in a.properties:
                                    ent['name'] = a.properties['name']

                            ents.append(ent)
                        real_classes = {e.get('identifier', e.get('name')) for e in ents if
                                        e['class'] not in ['Location', 'Specie']}
                        if len(real_classes) > 1:
                            output_sents.append(output_sent)
        sherpa_stem = pubmed_gz.stem.replace(".xml", "_sherpa")
        json_file = pubmed_gz.with_name(sherpa_stem + ".json")
        dl = DocumentList(__root__=docs)
        with json_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
        opennre_stem = pubmed_gz.stem.replace(".xml", "_opennre")
        json_file = pubmed_gz.with_name(opennre_stem + ".json")
        with json_file.open("w") as fout:
            json.dump(output_sents, fout, indent=2)


def analyze_annots(source, target, annots):
    bel_annots = defaultdict(list)
    for a in annots:
        found = {}
        found['source'] = fuzzy_find_in_annot(source, a)
        found['target'] = fuzzy_find_in_annot(target, a)
        for key, val in found.items():
            if val is not None:
                if 'function' in val and 'concept' in val:
                    bel_annots[key].append(a)
                    if a.label == 'Protein':
                        pmods = []
                        extract_pmods(source if key == 'source' else target, pmods)
                        if pmods:
                            if 'pmods' not in a.properties:
                                a.properties['pmods'] = set()
                            for pmod in pmods:
                                pmod_concept = pmod.type['concept']
                                pm = find_pmod_type(pmod_concept['name'])
                                if pm is not None:
                                    a.properties['pmods'].add(pm)
    return bel_annots['source'], bel_annots['target']


def filter_annotations(input: Document):
    def get_sort_key(a: Annotation):
        return a.end - a.start, -a.start

    sorted_annotations: Iterable[Annotation] = sorted(input.annotations, key=get_sort_key, reverse=True)
    seen_offsets = RangeMap()
    for ann in sorted_annotations:
        # Check for end - 1 here because boundaries are inclusive
        if seen_offsets.get(ann.start) is None and seen_offsets.get(ann.end - 1) is None:
            if ann.text is None:
                ann.text = input.text[ann.start:ann.end]
            seen_offsets[ann.start:ann.end] = ann
        else:
            target = seen_offsets.get(ann.start) or seen_offsets.get(ann.end - 1)
            # if target.labelName in kb_labels and ann.labelName in white_labels and (target.start-ann.start != 0 or target.end-ann.end != 0):
            if ann.labelName == 'modtype':
                seen_offsets.delete(target.start, target.end)
                seen_offsets[ann.start:ann.end] = ann
            elif ann.labelName == 'protein' and ann.properties:
                props = target.properties or {}
                props.update(ann.properties)
                target.properties = props
    result = sorted(seen_offsets.values(), key=lambda ann: ann.start)
    return result


def chunks(iterable, size=10):
    iterator = iter(iterable)
    for first in iterator:
        yield chain([first], islice(iterator, size - 1))


START_CHUNK = 0


@pytest.mark.skip(reason="Not a test")
def test_scai_eval_ef():
    def is_in(annot: Annotation, annots):
        for a in annots:
            if a.start == annot.start and a.end == annot.end and a.labelName == annot.labelName:
                return True
        return False

    def new_row(text, rel, h, t):
        return {
            'text': text,
            'relation': rel,
            'h': {
                'id': h.labelName,
                'name': h.properties.get('name', h.text),
                'pos': [h.start, h.end]
            },
            't': {
                'id': t.labelName,
                'name': t.properties.get('name', t.text),
                'pos': [t.start, t.end]
            }
        }

    testdir = Path(__file__).parent / 'data'
    token = get_token()
    linker = "ef"
    bel_parser = BELParser(skip_validation=True, citation_clearing=False, allow_naked_names=True)
    log_file = testdir / f"all_bell_relations_annotated_{linker}.log"
    with log_file.open("w") as log:
        json_file = testdir / "all_bell_relations.json"
        # json_file = testdir / f"one_bel_relation.json"
        with json_file.open("r") as fin:
            docs = json.load(fin)
        docs = [Document(**doc) for doc in docs]

        for i_chunk, list_docs in enumerate(chunks(docs, 100)):
            if i_chunk > START_CHUNK:
                rows = []
                for doc in list_docs:
                    annotated = annotate_with_ef(doc)
                    pmod_doc = annotate_with_pmod(doc, token)
                    if pmod_doc and pmod_doc.annotations:
                        annotated.annotations.extend(pmod_doc.annotations)
                        annotated.annotations = filter_annotations(annotated)
                    bel_sents = annotated.metadata.get("bel_sentences", [])
                    bels = []
                    for bel_sent in bel_sents:
                        try:
                            bels.append(bel_parser.parse(bel_sent))
                        except BaseException:
                            print(f"Invalid BEL sentence: {bel_sent}")
                            bels.append(None)
                    annotated.metadata["bels"] = bels
                    for a in annotated.annotations:
                        a.properties = a.properties or {}
                        forms = set()
                        forms.add(a.text.lower())
                        forms.add(a.text.translate(greek2latin).lower())
                        if a.properties and 'name' in a.properties and a.properties['name']:
                            forms.add(a.properties['name'].lower())
                        a.properties['forms'] = forms
                        a.properties['qualifiers'] = []
                    for ibel, bel in enumerate(annotated.metadata['bels']):
                        if bel is not None:
                            bel_sentence = annotated.metadata['bel_sentences'][ibel]
                            source = bel['source']
                            target = bel['target']
                            src_annots, tgt_annots = analyze_annots(source, target, annotated.annotations)
                            if src_annots or tgt_annots:
                                considered = [a for a in annotated.annotations
                                              if
                                              a.labelName in ['protein', 'abundance', 'biologicalprocess', 'pathology',
                                                              'modtype']
                                              or is_in(a, src_annots) or is_in(a, tgt_annots)]
                                for a1, a2 in combinations(considered, 2):
                                    is_src1 = is_in(a1, src_annots)
                                    is_tgt2 = is_in(a2, tgt_annots)
                                    is_src2 = is_in(a2, src_annots)
                                    is_tgt1 = is_in(a1, tgt_annots)
                                    is_pmod1 = a1.labelName == 'modtype' and 'name' in a1.properties
                                    is_pmod2 = a2.labelName == 'modtype' and 'name' in a2.properties
                                    is_prot1 = a1.labelName == 'protein' and 'name' in a1.properties
                                    is_prot2 = a2.labelName == 'protein' and 'name' in a2.properties
                                    if is_src1 and is_tgt2:
                                        rows.append(new_row(annotated.text, bel['relation'], a1, a2))
                                    elif is_src2 and is_tgt1:
                                        rows.append(new_row(annotated.text, bel['relation'], a2, a1))
                                    else:
                                        if is_prot1 and is_pmod2 and a2.properties['name'] in a1.properties.get('pmods',
                                                                                                                []):
                                            rows.append(new_row(annotated.text, 'modifies', a2, a1))
                                        elif is_prot2 and is_pmod1 and a1.properties['name'] in a2.properties.get(
                                                'pmods', []):
                                            rows.append(new_row(annotated.text, 'modifies', a1, a2))
                                        else:
                                            rows.append(new_row(annotated.text, 'NoRelation', a1, a2))
                                            rows.append(new_row(annotated.text, 'NoRelation', a2, a1))
                            else:
                                print(f"Not found in sentence: {annotated.text}", file=log)
                                print(f"BEL sentence: {bel_sentence}", file=log)
                                if not src_annots:
                                    print(f"\t- {source}", file=log)
                                if not tgt_annots:
                                    print(f"\t- {target}", file=log)
                json_file = testdir / f"all_bell_relations_matched_{linker}_{i_chunk}.json"
                with json_file.open("w") as fout:
                    for row in rows:
                        print(json.dumps(row), file=fout)
            else:
                print("SKIP")
