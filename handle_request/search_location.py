from analysis.ordinary_list_squares.k_means_clustering import find_centers
from analysis.ordinary_list_squares.count_claster_so import count_cluster_so_by_months
import numpy as np


class Searcher:

    def __init__(self, classifier):
        self.classifier = classifier

        tweets_with_so = classifier.calculate_summary_so()

        tweet_links = {index: value
                       for index, value in enumerate(tweets_with_so)
                       }

        X = np.array([(key, tweet.get('coordinates')[0], tweet.get('coordinates')[0])
                     for key, tweet in tweet_links.items()])

        centers, clusters = find_centers(X, 20)  # Fixed number of elements
        count_cluster_so_by_months(centers, clusters, tweet_links)
