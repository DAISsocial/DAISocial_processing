import math
import operator
import string
from collections import Counter
from collections import defaultdict

from nltk.corpus import stopwords

from analysis.collecting_data.collecting_tweets import TwitterCollector
from analysis.sentiment.tokenize import preprocess


class MediaClassifier:

    def __init__(self, data):

        self.count_all = Counter()
        self.center = data.get('center')
        self.radius = data.get('radius') if 'radius' in data else None
        self.com = defaultdict(lambda: defaultdict(int))

    def get_terms(self):

        collector = TwitterCollector(self.center, self.radius)
        tweets, radius = collector.search()

        for tweet in tweets:

            punctuation = list(string.punctuation)

            stop = stopwords.words('english') + punctuation + ['rt', 'via']
            # getting tweet tokenize words without stop words
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
        terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)

        print(terms_max[:5])
