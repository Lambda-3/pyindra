import requests
import json
from enum import Enum

#PARAMS
URL = "url"
PORT = "port"
DIR = "dir"
LANG = "language"
CORPUS = "corpus"
MODEL = "model"
TERM_COMPOSITION = "termComposition"
TRANSLATION_COMPOSITION = "translationComposition"
MT = "mt"
SCORE_FUNCTION = "scoreFunction"
PREPROCESSING = "preprocessing"

PAIRS = "pairs"
TERMS = "terms"
ONE = "one"
MANY = "many"

TOPK = "topk"
FILTER = "filter"

#URLS
POST_RELATEDNESS_PAIR = "{}/relatedness"
POST_RELATEDNESS_ONE_TO_MANY = "{}/relatedness/otm"

POST_VECTORS = "{}/vectors"

POST_NEIGHBORS_RELATEDNESS = "{}/neighbors/relatedness"
POST_NEIGHBORS_VECTORS = "{}/neighbors/vectors"

GET_VERSION = "{}/info/version"
GET_RESOURCES = "{}/info/resources"
GET_RESOURCE_INFO = "{}/info/resources/{}"

class NeighborsType(Enum):
    RELATEDNESS = 0
    VECTORS = 1

class IndraException(Exception):

    def __init__(self, message):
        self.message = message

class Indra:

    def __init__(self, url=None, port=8916, dir=None, lang="en", corpus="googlenews300neg", model="w2v",
                 term_composition=None, translation_composition=None, mt=False, score_function="COSINE", preprocessing=dict()):
        self._url = "{}:{}".format(url, port)
        self._headers = {'accept': "application/json", 'content-type': "application/json", 'cache-control': "no-cache"}
        self._base_data = {CORPUS : corpus, MODEL : model, LANG : lang, MT : mt}#, PREPROCESSING : preprocessing}
        self._score_function = score_function
        if term_composition is not None:
            self._base_data[TERM_COMPOSITION] = term_composition
        if translation_composition is not None:
            self._base_data[TRANSLATION_COMPOSITION] = translation_composition

    def _submit(self, url, payload=None):
        if payload is None:
            res = requests.get(url, headers=self._headers)
        else:
            res = requests.post(url, data=json.dumps(payload), headers=self._headers)

        if res.status_code == 200:
            return res.json()
        else:
            raise IndraException(res.content.decode("utf-8"))

    def _get_payload(self, pairs=None, one=None, many=None, terms=None):
        payload = self._base_data.copy()
        if pairs is not None:
            payload[SCORE_FUNCTION] = self._score_function
            if not isinstance(pairs, list):
                payload[PAIRS] = [pairs]
            else:
                payload[PAIRS] = pairs

        elif terms is not None:
            if not isinstance(terms, list):
                payload[TERMS] = [terms]
            else:
                payload[TERMS] = terms
        else:
            payload[SCORE_FUNCTION] = self._score_function
            payload[ONE] = one
            if not isinstance(many, list):
                payload[MANY] = [many]
            else:
                payload[MANY] = many

        return payload

    def service_version(self):
        return self._submit(GET_VERSION.format(self._url))["version"]


    def resources(self):
        return self._submit(GET_RESOURCES.format(self._url))

    def resource_info(self, resource):
        return self._submit(GET_RESOURCE_INFO.format(self._url, resource))

    def configure(self, configuration):
        for key in configuration:
            if key != PREPROCESSING:
                self._base_data[key] = configuration[key]
            else:
                for pk in configuration[key]:
                    self._base_data[key][pk] = configuration[key][pk]

    def vectors(self, terms):
        return self._submit(POST_VECTORS.format(self._url), self._get_payload(terms=terms))[TERMS]

    def relatedness(self, t1=None, t2=None, one=None, many=None, pairs=None):
        if pairs is None and one is None and many is None and t1 is not None and t2 is not None:
            return self._submit(POST_RELATEDNESS_PAIR.format(self._url),
                                self._get_payload(pairs={"t1":t1, "t2":t2}))[PAIRS][0]['score']

        elif pairs is not None and one is None and many is None and t1 is None and t2 is None:
            return self._submit(POST_RELATEDNESS_PAIR.format(self._url), self._get_payload(pairs=pairs))[PAIRS]

        elif pairs is None and one is not None and many is not None and t1 is None and t2 is None:
            return self._submit(POST_RELATEDNESS_ONE_TO_MANY.format(self._url), self._get_payload(one=one, many=many))

    def nearest_neighbors(self, terms, type=NeighborsType.VECTORS, topk=10, filter=None):
        if isinstance(topk, int) and topk > 0:
            payload = self._get_payload(terms=terms)
            payload[TOPK] = topk
            payload[FILTER] = filter

            if type == NeighborsType.VECTORS:
                return self._submit(POST_NEIGHBORS_VECTORS.format(self._url), payload)[TERMS]
            elif type == NeighborsType.RELATEDNESS:
                payload[SCORE_FUNCTION] = self._score_function
                return self._submit(POST_NEIGHBORS_RELATEDNESS.format(self._url), payload)[TERMS]
            else:
                raise IndraException("'{}' is not a valid type. Please use the enum 'NeighborsType'".format(type))
        else:
            raise IndraException("'top' must be an integer higher than 0")


