import datetime


"""
Counting cluster semantic orientation
"""


def count_cluster_so_by_months(mu, cl, my_dict):
    clusters_by_months = []
    for index in enumerate(mu):

        max_distance = 0

        cluster_months = {
            '30': (0, 0),
            '60': (0, 0),
            '90': (0, 0),
            '120': (0, 0),
            'distance': 0
        }
        for node in cl[index]:

            current_tweet = my_dict[node[0]]
            days_delta = (datetime.datetime.now() - current_tweet.get('created_at')).days

            if days_delta <= 30:
                cluster_months['30'][0] += 1
                cluster_months['30'][1] += current_tweet.get('semantic_orientation') * (
                    0.5 * current_tweet.get('likes') + current_tweet.get('retweets'))
            elif days_delta <= 60:
                cluster_months['30'][0] += 1
                cluster_months['60'][1] += current_tweet.get('semantic_orientation') * (
                    0.5 * current_tweet.get('likes') + current_tweet.get('retweets'))
            elif days_delta <= 90:
                cluster_months['90'][0] += 1
                cluster_months['90'][1] += current_tweet.get('semantic_orientation') * (
                    0.5 * current_tweet.get('likes') + current_tweet.get('retweets'))
            elif days_delta <= 120:
                cluster_months['120'][0] += 1
                cluster_months['120'][1] += current_tweet.get('semantic_orientation') * (
                    0.5 * current_tweet.get('likes') + current_tweet.get('retweets'))

