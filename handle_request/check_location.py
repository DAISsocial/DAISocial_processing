from analysis.sentiment.sentiment_analysis import MediaClassifier
from matplotlib.dates import date2num
import matplotlib.pyplot as plt
import numpy as np
import datetime
from reports.check_location_report import CheckReport
from matplotlib.dates import DayLocator, HourLocator, DateFormatter
from numpy import arange


class Checker:

    def __init__(self, classifier: MediaClassifier):
        self.classifier = classifier
        self.classifier.calculate_semantic_orientation()

    def all_media(self):
        tweets_by_date = {}
        for tweet in self.classifier.tweets:
            if str(tweet.created_at.date()) not in tweets_by_date:
                tweets_by_date[str(tweet.created_at.date())] = 1
            else:
                tweets_by_date[str(tweet.created_at.date())] += 1

        x = np.array([date2num(datetime.datetime.strptime(key, '%Y-%m-%d').date())
                      for key in tweets_by_date.keys()])
        x.sort()
        y = np.array([value for value in tweets_by_date.values()])

        fig, ax = plt.subplots()
        ax.plot_date(x, y, '-')

        ax.set_xlim(x[0], x[-1])

        ax.xaxis.set_major_locator(DayLocator())
        ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

        ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
        fig.autofmt_xdate()

        return plt.savefig('plots/plot.png')

    def competitor_media(self):
        return {term: self.classifier.semantic_orientation[term]
                for term in self.classifier.request_type.get('keywords')
                if term in self.classifier.semantic_orientation}

    def last_media(self):
        return {'most_common': self.classifier.count_all.most_common(5),
                'terms_max': self.classifier.terms_max[:5]}

    def run(self):
        graphic = self.all_media()
        media_most_common = self.last_media()
        competitor_media = self.competitor_media()

        report = CheckReport()
        report.create(graphic, media_most_common, competitor_media)
        report.save(filename='demo.docx')
