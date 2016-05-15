import math
import operator
import string
from collections import Counter
from collections import defaultdict

from nltk.corpus import stopwords

from analysis.sentiment.tokenize import preprocess
from .base import MediaClassifier


class CompetitorMediaClassifier(MediaClassifier):

    def __init__(self, data, request_type):

        super().__init__(data)

        self.n_docs = 0  # count of tweets collected
        self.positive_vocab = []
        self.negative_vocab = []
        self.pmi = defaultdict(lambda: defaultdict(int))

        self.generate_vocabularies(request_type)

        # Probabilities P(t)
        self.p_t = {}
        # Probabilities P(t1, t2)
        self.p_t_com = defaultdict(lambda: defaultdict(int))

    def compute_probabilities(self):

        for term, n in self.count_all.items():
            self.p_t[term] = n / self.n_docs
            for t2 in self.com[term]:
                self.p_t_com[term][t2] = self.com[term][t2] / self.n_docs

    def generate_vocabularies(self, request_type):
        positive_vocab = [
            'good', 'nice', 'great', 'awesome', 'outstanding',
            'fantastic', 'terrific', ':)', ':-)', 'like', 'love',
            # shall we also include game-specific terms?
            # 'triumph', 'triumphal', 'triumphant', 'victory', etc.
        ]
        # adding specific vocab from request
        self.positive_vocab = positive_vocab.extend(request_type.get('positive_verbs'))

        negative_vocab = [
            'bad', 'terrible', 'crap', 'useless', 'hate', ':(', ':-(',
            # 'defeat', etc.
        ]
        # adding specific vocab from request
        self.negative_vocab = negative_vocab.extend(request_type.get('negative_verbs'))

    def calculate_semantic_orientation(self):

        for t1 in self.p_t:
            for t2 in self.com[t1]:
                denom = self.p_t[t1] * self.p_t[t2]
                self.pmi[t1][t2] = math.log2(self.p_t_com[t1][t2] / denom)

        semantic_orientation = {}
        for term, n in self.p_t.items():
            positive_assoc = sum(self.pmi[term][tx] for tx in self.positive_vocab)
            negative_assoc = sum(self.pmi[term][tx] for tx in self.negative_vocab)
            semantic_orientation[term] = positive_assoc - negative_assoc

        semantic_sorted = sorted(semantic_orientation.items(),
                                 key=operator.itemgetter(1),
                                 reverse=True)

        top_pos = semantic_sorted[:10]
        top_neg = semantic_sorted[-10:]


def competitor_media_process(data: dict, request_type: dict):
    my_clsf = CompetitorMediaClassifier(data, request_type)
    most_common = my_clsf.get_terms()



