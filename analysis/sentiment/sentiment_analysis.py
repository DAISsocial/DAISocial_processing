import math
import operator
import string
from collections import Counter
from collections import defaultdict

from nltk.corpus import stopwords

from analysis.sentiment.tokenize import preprocess
from collecting_data.collecting_tweets import TwitterCollector


from config.mode import CACHED_MODE


class MediaClassifier:

    def __init__(self, data, request_type):

        self.count_all = Counter()
        self.center = data.get('center')
        self.radius = data.get('radius') if 'radius' in data else None
        self.com = defaultdict(lambda: defaultdict(int))

        self.n_docs = 0  # count of tweets collected
        self.positive_vocab = []
        self.negative_vocab = []
        self.pmi = defaultdict(lambda: defaultdict(int))

        self.request_type = request_type
        self.generate_vocabularies()

        # Probabilities P(t)
        self.p_t = {}
        # Probabilities P(t1, t2)
        self.p_t_com = defaultdict(lambda: defaultdict(int))
        self.semantic_orientation = {}

        self.tweets = None
        self.terms_max = None

    def get_terms(self, last_days=False):

        collector = TwitterCollector(self.center, self.radius, CACHED_MODE)
        self.tweets, radius = collector.search_last_days() \
            if last_days else collector.search()

        self.n_docs = len(self.tweets)

        for tweet in self.tweets:

            punctuation = list(string.punctuation)

            stop = stopwords.words('english') + punctuation + ['rt', 'via']
            # getting tweet tokenize words without stop words
            if last_days:
                terms_all = [term for term in preprocess(tweet.get('text'))
                             if term not in stop and not term.startswith('@')]
            else:
                terms_all = [term for term in preprocess(tweet.text)
                             if term not in stop and not term.startswith('@')]

            self.count_all.update(terms_all)

            # Build co-occurrence matrix
            for i in range(len(terms_all)-1):
                for j in range(i+1, len(terms_all)):
                    w1, w2 = sorted([terms_all[i], terms_all[j]])
                    if w1 != w2:
                        self.com[w1][w2] += 1

        return self.count_all.most_common(5)  # 5 !!!!!!!!!!!

    def most_frequent(self):

        com_max = []
        # For each term, look for the most common co-occurrent terms
        for t1 in self.com:

            t1_max_terms = sorted(self.com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
            for t2, t2_count in t1_max_terms:

                com_max.append(((t1, t2), t2_count))

        # Get the most frequent co-occurrences
        self.terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)

        print(self.terms_max[:5])

    def compute_probabilities(self):

        for term, n in self.count_all.items():
            self.p_t[term] = n / self.n_docs
            for t2 in self.com[term]:
                self.p_t_com[term][t2] = self.com[term][t2] / self.n_docs

    def generate_vocabularies(self):
        positive_vocab = [
            'good', 'nice', 'great', 'awesome', 'outstanding',
            'fantastic', 'terrific', ':)', ':-)', 'like', 'love',
            # shall we also include game-specific terms?
            # 'triumph', 'triumphal', 'triumphant', 'victory', etc.
        ]
        # adding specific vocab from request
        self.positive_vocab = positive_vocab + self.request_type.get('positive_verbs')

        negative_vocab = [
            'bad', 'terrible', 'crap', 'useless', 'hate', ':(', ':-(',
            # 'defeat', etc.
        ]
        # adding specific vocab from request
        self.negative_vocab = negative_vocab + self.request_type.get('negative_verbs')

    def calculate_semantic_orientation(self, last_days=False):

        self.get_terms(last_days=last_days)
        self.most_frequent()
        self.compute_probabilities()

        for t1 in self.p_t:
            for t2 in self.com[t1]:
                denom = self.p_t[t1] * self.p_t[t2]
                self.pmi[t1][t2] = math.log2(self.p_t_com[t1][t2] / denom)

        for term, n in self.p_t.items():
            positive_assoc = sum(self.pmi[term][tx] for tx in self.positive_vocab
                                 if self.pmi[term][tx])
            negative_assoc = sum(self.pmi[term][tx] for tx in self.negative_vocab
                                 if self.pmi[term][tx])
            self.semantic_orientation[term] = positive_assoc - negative_assoc

        semantic_sorted = sorted(self.semantic_orientation.items(),
                                 key=operator.itemgetter(1),
                                 reverse=True)

        top_pos = semantic_sorted[:10]
        top_neg = semantic_sorted[-10:]

    def calculate_summary_so(self):

        self.calculate_semantic_orientation(last_days=True)

        for tweet in self.tweets:
            punctuation = list(string.punctuation)

            stop = stopwords.words('english') + punctuation + ['rt', 'via']
            # getting tweet tokenize words without stop words
            terms_all = [term for term in preprocess(tweet.get('text'))
                         if term not in stop and not term.startswith('@')]

            if type(tweet) is dict:
                so = 0
                for term in terms_all:
                    so += self.semantic_orientation[term] if term in self.semantic_orientation else 0
                tweet['semantic_orientation'] = so

        return self.tweets
