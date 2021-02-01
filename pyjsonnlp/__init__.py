#!/usr/bin/env python3

"""
(C) 2020-2021 by Semiring Inc., Damir Cavar <damir@semiring.com>

The JSON-NLP specification had contributions to earlier versions by Oren Baldinger,
Maanvitha Gongalla, Anurag Kumar, Murali Kammili

Functions for manipulating and expanding a JSON-NLP object

Licensed under the Apache License 2.0, see the file LICENSE for more details.
"""

import json
from json import JSONEncoder
import datetime
from collections import OrderedDict
from typing import List
import copy

name = "pyjsonnlp"
__version__ = "0.7"


def get_base() -> OrderedDict:
    """
    Return a base framework for JSON-NLP.
    :returns Base frame for a JSON-NLP object
    :rtype OrderedDict
    """

    return OrderedDict({
        "meta": {
            "DC.conformsTo": __version__,
            "DC.author": "",
            "DC.source": "",  # where did the corpus come from
            "DC.created": datetime.datetime.now().replace(microsecond=0).isoformat(),
            "DC.date": datetime.datetime.now().replace(microsecond=0).isoformat(),
            "DC.creator": "",
            'DC.publisher': "",
            "DC.title": "",
            "DC.description": "",
            "DC.identifier": "",
            "DC.language": "",
            "DC.subject": "",
            "DC.contributors": "",
            "DC.type": "",
            "DC.format": "",
            "DC.relation": "",
            "DC.coverage": "",
            "DC.rights": "",
            "counts": {},
        },
        "conll": {},
        "documents": []
    })


def get_base_document(doc_id: int) -> OrderedDict:
    """Returns a JSON base document."""

    return OrderedDict({
        "meta": {
            "DC.conformsTo": __version__,
            "DC.author": "",
            "DC.source": "",  # where did the corpus come from
            "DC.created": datetime.datetime.now().replace(microsecond=0).isoformat(),
            "DC.date": datetime.datetime.now().replace(microsecond=0).isoformat(),
            "DC.creator": "",
            'DC.publisher': "",
            "DC.title": "",
            "DC.description": "",
            "DC.identifier": "",
            "DC.language": "",
            "DC.subject": "",
            "DC.contributors": "",
            "DC.type": "",
            "DC.format": "",
            "DC.relation": "",
            "DC.coverage": "",
            "DC.rights": "",
            "counts": {},
        },
        "id": doc_id,
        "conllId": "",
        "text": "",
        "tokenList": [],
        "clauses": [],
        "sentences": [],
        "paragraphs": [],
        "dependencies": [],
        "coreferences": [],
        "constituents": [],
        "expressions": [],
    })


def remove_empty_fields(json_nlp: OrderedDict) -> OrderedDict:
    """Remove empty fields from root, meta, and documents"""
    cleaned = OrderedDict()
    for k, v in json_nlp.items():
        if v != '' and v != [] and v != {}:
            cleaned[k] = v
    if 'meta' in cleaned:
        cleaned['meta'] = remove_empty_fields(cleaned['meta'])
    if 'documents' in cleaned:
        # for i, d in cleaned['documents'].items():
        for i in range(len(cleaned['documents'])):
            cleaned['documents'][i] = remove_empty_fields(cleaned['documents'][i])
    return cleaned


def find_head(doc: OrderedDict, token_ids: List[int], sentence_id: int, style='universal') -> int:
    """
    Given phrase, clause, or other group of token ids, use a dependency parse to find the head token.
    We create two sets, governors and dependents of the tokens in token_ids. The elements in gov that do not occur
    in dependents are the heads. There should be just one.
    """
    # print(sentence_id, doc['dependencies'],doc['dependencies']['trees'])
    if len(token_ids) == 0:
        return None
    arcs = doc['dependencies'][sentence_id - 1]['trees']
    govs = set(token_ids)
    for x in arcs:
        if x["dep"] in govs and x["gov"] in govs:
            govs.remove(x["dep"])
    govs = list(govs)
    if len(govs) == 0:
        return None
    return govs[0]


def build_coreference(reference_id: int) -> dict:
    """Build a frame for a coreference structure"""

    return {
        'id': reference_id,
        'representative': {
            'tokens': []
        },
        'referents': []
    }


def build_constituents(sent_id: int, s: str) -> dict:
    """ """
    s = s.rstrip().lstrip()
    open_bracket = s[0]  # ( or [
    close_bracket = s[-1]  # ) or ]
    return {
        'sentenceId': sent_id,
        'labeledBracketing': f'{open_bracket}ROOT {s}{close_bracket}' if s[1:5] != 'ROOT' else s
    }


class MyOrderedDict(OrderedDict):
    """ """
    def __init__(self, *args, **kwargs):
        super(MyOrderedDict, self).__init__(*args, **kwargs)

    def toJSON(self) -> str:
        """A generic toJSON method for linerization of all but the None valued attributes."""
        return json.loads(json.dumps(OrderedDict([(k, v) for (k, v) in self.items() if v is not None]),
                                     default=lambda o: o.__dict__,
                                     indent=3))


# subclass JSONEncoder
class DocumentEncoder(JSONEncoder):
    def default(self, o):
        myJSON = json.loads("[]")
        myJL = [o["meta"]]
        return json.dumps(OrderedDict([(k, v) for (k, v) in self.items() if v is not None]),
                          default=lambda o: o.__dict__,
                          indent=3)
        # return o.__dict__


class TokenFeatures(MyOrderedDict):
    """ """

    def __init__(self):
        super().__init__()
        self.overt = -1  # bool
        self.stop = -1  # bool
        self.alpha = -1  # bool,omitempty
        self.number = -1  # int, omitempty - 1 = singular, 2 = dual, 3 or more = plural
        self.gender = ""  # string, omitempty - male, female, neuter
        self.person = -1  # int, omitempty - 1, 2, 3
        self.tense = ""  # string, omitempty - past, present, future
        self.perfect = -1  # bool, omitempty"`
        self.continuous = -1  # bool, omitempty"`
        self.case = ""  # string, omitempty - nom, acc, dat, gen, voc, loc, inst, ...
        self.human = -1  # bool, omitempty - yes/no
        self.animate = -1  # bool, omitempty - yes/no
        self.negated = -1  # bool, omitempty - word in scope og negation
        self.countable = -1  # bool, omitempty
        self.factive = -1  # bool, omitempty - factive verb
        self.counterfactive = -1  # bool, omitempty
        self.irregular = -1  # bool, omitempty - irregular verb or noun form
        self.phrasalVerb = -1  # bool, omitempty
        self.mood = -1  # string, omitempty - indicative, imperative, subjunctive
        self.foreign = -1  # bool, omitempty
        self.spaceAfter = -1  # bool, omitempty


class Token:
    """ """

    def __init__(self, id, sentenceID):
        self.id = id
        self.sentence_id = sentenceID
        self.text = ""  # string - "went"
        self.lemma = ""  # string, omitempty - "go"
        self.xpos = ""  # string, omitempty - "NNP"
        self.xpos_prob = -1.0  # float, omitempty
        self.upos = ""  # string, omitempty - "PROPN"
        self.upos_prob = -1.0  # float, omitempty
        self.entity_iob = ""  # string, omitempty - "B"
        self.characterOffsetBegin = -1  # , omitempty
        self.characterOffsetEnd = -1  # , omitempty
        self.propID = ""  # , omitempty - PropBank ID
        self.propIDProbability = -1.0  # , omitempty - PropBank ID probability
        self.frameID = -1  # , omitempty
        self.frameID = -1.0  # , omitempty
        self.wordNetID = -1  # , omitempty
        self.wordNetID = -1.0  # , omitempty
        self.verbNetID = -1  # , omitempty
        self.verbNetID = -1.0  # , omitempty
        self.lang = ""  # , omitempty - "en"
        self.features = TokenFeatures  # , omitempty
        self.shape = ""  # , omitempty - "Xxxx"
        self.entity = ""  # , omitempty - "PERSON"


class Sentence:
    """Sentence properties in JSON-NLP."""

    def __init__(self, id):
        self.id = id  # int
        self.tokenFrom = -1  # int, omitempty
        self.tokenTo = -1  # int, omitempty
        self.tokens = []  # list of ints, omitempty
        self.clauses = []  # list of ints, omitempty
        self.type = ""  # string, omitempty - type of sentence: declarative, interrogative, exclamatory, imperative, instructive
        self.sentiment = ""  # string, omitempty - sentiment label
        self.sentimentProb = -1.0  # float, omitempty


class Clause:
    """Clause properties in JSON-NLP."""

    def __init__(self, id, sentenceID):
        self.id = id  # int
        self.sentenceID = sentenceID  # int
        self.tokenFrom = -1  # int, omitempty
        self.tokenTo = -1  # int, omitempty
        self.tokens = []  # list of ints, omitempty
        self.main = -1  # bool, omitempty
        self.gov = -1  # int, omitempty
        self.head = -1  # int, omitempty
        self.neg = -1  # bool, omitempty
        self.tense = ""  # string, omitempty
        self.mood = ""  # string, omitempty
        self.aspect = ""  # string, omitempty
        self.voice = ""  # string, omitempty
        self.sentiment = ""  # string, omitempty
        self.sentimentProb = -1.0  # float, omitempty


class Dependency:
    """Dependency annotation in JSON-NLP."""

    def __init__(self):
        self.lab = ""  # string - label of dependency
        self.gov = -1  # int - token ID of governor
        self.dep = -1  # int - token ID of dependent
        self.prob = -1.0  # float, omitempty - probability of dependency


class DependencyTree:
    """ """

    def __init__(self):
        pass
    # SentenceID   int          `json:"sentenceID"`
    # Style        string       `json:"style,omitempty"`
    # Dependencies []Dependency `json:"dependencies,omitempty"`
    # Probability  float64      `json:"prob,omitempty"`


class CoreferenceRepresentantive:
    """ """

    def __init__(self):
        pass
    # Tokens []int `json:"tokens"`
    # Head   int   `json:"head,omitempty"`


class CoreferenceReferents:
    """ """

    def __init__(self):
        pass
    # Tokens      []int   `json:"tokens"`
    # Head        int     `json:"head,omitempty"`
    # Probability float64 `json:"prob,omitempty"`


class Coreference:
    """ """

    def __init__(self):
        pass
    # ID             int                        `json:"id"`
    # Representative CoreferenceRepresentantive `json:"representative"`
    # Referents      []CoreferenceReferents     `json:"referents"`


class Scope:
    """ """

    def __init__(self):
        pass
    # ID         int   `json:"id"`
    # Governor   []int `json:"gov"`
    # Dependents []int `json:"dep,omitempty"`
    # Terminals  []int `json:"terminals,omitempty"`


class ConstituentParse:
    """ """

    def __init__(self):
        pass
    # SentenceID        int     `json:"sentenceId"`
    # Type              string  `json:"type,omitempty"`
    # LabeledBracketing string  `json:"labeledBracketing"`
    # Probability       float64 `json:"prob,omitempty"`
    # Scopes            []Scope `json:"scopes,omitempty"`


class Expression:
    """ """

    def __init__(self):
        pass
    # ID          int     `json:"id"`
    # Type        string  `json:"type,omitempty"` // "NP"
    # Head        int     `json:"head,omitempty"`
    # Dependency  string  `json:"dependency,omitempty"` // "nsubj"
    # TokenFrom   int     `json:"tokenFrom,omitempty"`  // first token
    # TokenTo     int     `json:"tokenTo,omitempty"`    // last token
    # Tokens      []int   `json:"tokens"`
    # Probability float64 `json:"prob,omitempty"`


class Paragraph:
    """ """

    def __init__(self):
        pass
    # ID        int   `json:"id"`
    # TokenFrom int   `json:"tokenFrom,omitempty"`
    # TokenTo   int   `json:"tokenTo,omitempty"`
    # Tokens    []int `json:"tokens,omitempty"`
    # Sentences []int `json:"sentences,omitempty"`


class Attribute:
    """ """

    def __init__(self):
        pass
    # Label string `json:"lab"`
    # Value string `json:"val"`


class Entity:
    """ """

    def __init__(self):
        pass
    # ID                   int         `json:"id"`
    # Label                string      `json:"label"`
    # Type                 string      `json:"type"`
    # Sentiment            string      `json:"sentiment,omitempty"`     //
    # SentimentProbability float64     `json:"sentimentProb,omitempty"` //
    # Attributes           []Attribute `json:"attributes"`


class Relation:
    """ """

    def __init__(self):
        pass
    # ID                   int         `json:"id"`
    # Label                string      `json:"label"`
    # Type                 string      `json:"type"`
    # Sentiment            string      `json:"sentiment,omitempty"`     //
    # SentimentProbability float64     `json:"sentimentProb,omitempty"` //
    # Attributes           []Attribute `json:"attributes"`


class Triple(OrderedDict):
    """Triple annotation in JSON-NLP."""

    # declare the fields and types here:
    types = OrderedDict([("clauseID", 1),
                         ("fromEntity", 1),
                         ("toEntity", 1),
                         ("rel", 1),
                         ("sentenceID", 1),
                         ("directional", True),
                         ("eventID", 1),
                         ("tempSeq", 1),
                         ("prob", 0.1),
                         ("syntactic", True),
                         ("implied", True),
                         ("presupposed", True)])

    def __init__(self, clauseID: int, fromEntity: int, toEntity: int, rel: int):
        super(Triple, self).__init__(OrderedDict.fromkeys(self.types, None))
        self["clauseID"] = clauseID
        self["fromEntity"] = fromEntity
        self["toEntity"] = toEntity
        self["rel"] = rel

    def __setitem__(self, key, value):
        if key in self.types:
            if value is None or isinstance(value, type(self.types[key])):
                super().__setitem__(key, value)
        # self.move_to_end(key)

    def setClauseID(self, id: int):
        self["clauseID"] = id

    def getClauseID(self) -> int:
        return self["clauseID"]

    def setFromEntity(self, f: int):
        self["fromEntity"] = f

    def getFromEntity(self) -> int:
        return self["fromEntity"]

    def setToEntity(self, t: int):
        self["toEntity"] = t

    def getToEntity(self) -> int:
        return self["toEntity"]

    def setRel(self, r: int):
        self["rel"] = r

    def getRel(self) -> int:
        return self["rel"]

    def setSentenceID(self, id: int):
        self["sentenceID"] = id

    def getSentenceID(self) -> int:
        return self["sentenceID"]

    def setDirectional(self):
        self["directional"] = True

    def unsetDirectional(self):
        self["directional"] = None

    def getDirectional(self):
        return self["directional"]

    def setEventID(self, id: int):
        self["eventID"] = id

    def getEventID(self) -> int:
        return self["eventID"]

    def setTempSeq(self, s: int):
        self["tempSeq"] = s

    def getTempSeq(self) -> int:
        return self["tempSeq"]

    def setProb(self, p: float):
        self["prob"] = p

    def getProb(self) -> float:
        return self["prob"]

    def setPresupposed(self):
        self["presupposed"] = True

    def unsetPresupposed(self):
        self["presupposed"] = None

    def getPresupposed(self):
        return self["presupposed"]

    def setImplied(self):
        self["implied"] = True

    def unsetImplied(self):
        self["implied"] = None

    def getImplied(self):
        return self["implied"]

    def setSyntactic(self):
        self["syntactic"] = True

    def unsetSyntactic(self):
        self["implied"] = None

    def getSyntactic(self):
        return self["implied"]

    def toJSON(self) -> str:
        return json.loads(json.dumps(OrderedDict([(k, v) for (k, v) in self.items() if v is not None]),
                                     default=lambda o: o.__dict__,
                                     indent=3))

class Meta(MyOrderedDict):
    """ """

    # declare the fields and types here:
    types = {"DC.conformsTo": "",
             "DC.author": "",
             "DC.source": "",
             "DC.created": "",
             "DC.date": "",
             "DC.creator": "",
             "DC.publisher": "",
             "DC.title": "",
             "DC.description": "",
             "DC.identifier": "",
             "DC.language": "",
             "DC.subject": "",
             "DC.contributors": "",
             "DC.type": "",
             "DC.format": "",
             "DC.relation": "",
             "DC.coverage": "",
             "DC.rights": ""}

    def __init__(self):
        """ """
        super(Meta, self).__init__(OrderedDict.fromkeys(self.types, None))
        self["DC.conformsTo"] = __version__
        self["DC.created"] = datetime.datetime.now().replace(microsecond=0).isoformat()
        self["DC.date"] = datetime.datetime.now().replace(microsecond=0).isoformat()

    def toJSON(self) -> str:
        """ """
        return json.loads(json.dumps(OrderedDict([(k, v) for (k, v) in self.items() if v is not None]),
                                     default=lambda o: o.__dict__,
                                     indent=3))


class Document(MyOrderedDict):
    """Document properties in JSON-NLP."""

    # declare the fields and types here:
    types = {"meta": type(Meta()),
             "id": type(1),
             "tokenlist": [],
             "clauses": [],
             "sentences": [],
             "paragraphs": [],
             "dependencyTrees": [],
             "coreferences": [],
             "constituents": [],
             "expressions": [],
             "entities": [],
             "relations": [],
             "triples": []}

    def __init__(self, id):
        super(Document, self).__init__()
        # super(Meta, self).__init__(MyOrderedDict.fromkeys(self.types, None))
        self.meta = Meta()
        self.id = id
        self.tokenList = []
        self.clauses = []
        self.sentences = []
        self.paragraphs = []
        self.dependencyTrees = []
        self.coreferences = []
        self.constituents = []
        self.expressions = []
        self.entities = []
        self.relations = []
        self.triples = []

    def addClause(self, sentenceID):
        """Adds a new clause definition to the document in JSON-NLP."""
        self.clauses.append(Clause(len(self.clauses), sentenceID))

    def addSententce(self):
        pass

    def addParagrap(self):
        pass

    def addDependencyTree(self):
        pass

    def addCoreference(self):
        pass

    def addConstituent(self):
        pass

    def addExpression(self):
        pass

    def addEntity(self):
        pass

    def addRelation(self):
        pass

    def addTriple(self, triple=None):
        if triple is None:

            pass
        else:
            pass


class JSONNLP(MyOrderedDict):
    """JSON-NLP main class definition."""

    def __init__(self):
        super(JSONNLP, self).__init__()
        self.meta = Meta()
        self.documents = []

    def addDocument(self, doc=None):
        """Adds a new document to the JSON-NLP documents list."""
        if doc is None:
            self.documents.append(Document(len(self.documents)))
        elif isinstance(doc, type(Document)):
            self.documents.append(doc)


def main():
    mj = JSONNLP()
    md = Document(1)
    md.addTriple()
    mj.addDocument(md)
    mt = Triple(1, 2, 3, 4)
    mt.setClauseID(5)
    a = [mt.toJSON()]
    a.append(mt.toJSON())
    print(json.dumps(a, default=lambda o: o.__dict__, indent=3))  # mt.toJSON())
    mt.getDirectional()
    print(type(mt))
    # print(mt.toJSON())


if __name__ == '__main__':
    main()
