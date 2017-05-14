import datetime

import numpy as np
from ..analysis.k_means_clustering import find_centers
from geopy.distance import vincenty

from api.analysis.calculate_increase import calculate_increase
from reports.search_location_report import SearchReport


class Searcher:

    def __init__(self, classifier):
        self.centers = None
        self.clusters = None

        self.classifier = classifier
        self.cl_by_months = None

    def founding_best_cluster(self):
        tweets_with_so = self.classifier.calculate_summary_so()

        tweet_links = {
            index: value
            for index, value in enumerate(tweets_with_so)
        }

        X = np.array(
            [(key, tweet['coordinates'][0], tweet['coordinates'][1])
             for key, tweet in tweet_links.items()]
        )

        self.centers, self.clusters = find_centers(X, 20)  # Fixed number of elements
        self.cl_by_months = self.count_cluster_so_by_months(tweet_links)
        del self.centers, self.clusters

        best_cl = self.calculate_increase()
        return best_cl

    def count_cluster_so_by_months(self, tweet_links):
        clusters_by_months = []
        for index in enumerate(self.centers):

            cl_months = {
                '30': [0, 0],
                '60': [0, 0],
                '90': [0, 0],
                '120': [0, 0],
                'max_distance': 0,
                'center': tweet_links[index[0]].get('coordinates')
            }
            for node in self.clusters[index[0]]:

                current_tweet = tweet_links[node[0]]
                distance_delta = vincenty(current_tweet.get('coordinates'),
                                          cl_months['center']).meters
                if cl_months['max_distance'] < distance_delta:
                    cl_months['max_distance'] = distance_delta

                days_delta = (datetime.datetime.now() - current_tweet.get('created_at')).days

                if days_delta <= 30:
                    cl_months['30'][0] += 1
                    cl_months['30'][1] += current_tweet.get('semantic_orientation') * (
                        0.5 * current_tweet.get('likes') + current_tweet.get('retweets'))
                elif days_delta <= 60:
                    cl_months['30'][0] += 1
                    cl_months['60'][1] += current_tweet.get('semantic_orientation') * (
                        0.5 * current_tweet.get('likes') + current_tweet.get('retweets'))
                elif days_delta <= 90:
                    cl_months['90'][0] += 1
                    cl_months['90'][1] += current_tweet.get('semantic_orientation') * (
                        0.5 * current_tweet.get('likes') + current_tweet.get('retweets'))
                elif days_delta <= 120:
                    cl_months['120'][0] += 1
                    cl_months['120'][1] += current_tweet.get('semantic_orientation') * (
                        0.5 * current_tweet.get('likes') + current_tweet.get('retweets'))

            clusters_by_months.append(cl_months)

        return clusters_by_months

    def calculate_increase(self):

        best_cluster, max_a = None, np.iinfo(np.int16).min

        for cluster in self.cl_by_months:
            a1 = calculate_increase(
                np.array([cluster['30'][1],
                          cluster['60'][1],
                          cluster['90'][1],
                          cluster['120'][1]])
            )
            if a1 > max_a:
                best_cluster, max_a = cluster, a1

        return best_cluster

    def run(self):
        best_cluster = self.founding_best_cluster()

        report = SearchReport()
        report.create(best_cluster)
        report.save(filename='demo1.docx')
