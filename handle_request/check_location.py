from analysis.sentiment.sentiment_analysis import MediaClassifier
from matplotlib.dates import date2num
from matplotlib.pyplot import plot_date
import numpy as np


class Checker:

    def __init__(self, classifier: MediaClassifier):
        self.classifier = classifier
        self.classifier.calculate_semantic_orientation()

        self.all_media()
        self.last_media()

    def all_media(self):
        tweets_by_date = {}
        for tweet in self.classifier.tweets:
            if not tweets_by_date[tweet.created_at.date()]:
                tweets_by_date[tweet.created_at.date()] = 1
            else:
                tweets_by_date[tweet.created_at.date()] += 1

        x = np.array([date2num(key) for key in tweets_by_date.keys()])
        y = np.array([value for value in tweets_by_date.values()])
        plot_date(x, y, '-')

    def competitor_media(self):
        a = {term: self.classifier.semantic_orientation[term]
             for term in self.classifier.request_type.get('keywords')}

    def last_media(self):
        self.classifier.count_all.most_common(5)
        self.classifier.terms_max[:5]
