import asyncio
import datetime
import json
import random
import time

from tweepy import Cursor

from config import GLOBAL_CONFIG
from config.count import COUNT_TWEETS


class TwitterCollector:

    def __init__(self, center, radius=None, count=None, cached=False):
        self.center = center
        self.radius = radius
        self.count = count
        self.cached = cached

    def search(self):

        if not self.radius:
            self.radius = 2

        results = list()
        results_ids = set()
        converted_string = "{},{},{}km".format(
            self.center[0], self.center[1], self.radius)

        # while len(results) < 9000 and self.radius < 6:
        twitter_client = GLOBAL_CONFIG.twitter_client
        try:
            for tweet in Cursor(
                twitter_client.search,
                rpp=100,
                geocode=converted_string,
                show_user=False,
                result_type="recent",
                include_entities=True,
                lang="en"
            ).items(COUNT_TWEETS):  # Counts
                if tweet.id not in results_ids:
                    results.append(tweet)
                    results_ids.add(tweet.id)
            self.radius += 1
        except BaseException as e:
            time.sleep(20)

        return results, self.radius

    def search_last_days(self, days_count=120):

        if not self.cached:
            if not self.radius:
                self.radius = 2

            results = list()
            #flag = True
            #while flag:

            converted_string = "{},{},{}km".format(self.center[0],
                                                   self.center[1], self.radius)
            twitter_client = GLOBAL_CONFIG.twitter_client
            try:
                for tweet in Cursor(
                    twitter_client.search,
                    rpp=100,
                    geocode=converted_string,
                    show_user=False,
                    result_type="recent",
                    include_entities=True,
                    lang="en"
                ).items(COUNT_TWEETS):  # Count
                    days_delta = (datetime.datetime.now() - tweet.created_at).days

                    #if days_delta < days_count:
                    if tweet.coordinates:

                        tweet_structure = {
                            'text': tweet.text,
                            'coordinates':
                                [random.uniform(self.center[0] - 0.005, self.center[0] + 0.005),
                                 random.uniform(self.center[1] - 0.007, self.center[1] + 0.007)],
                            'likes': tweet.favorite_count,
                            'retweets': tweet.retweet_count,
                            'created_at': datetime.datetime.strptime("2017-{}-{}".format(random.randint(2, 5),
                                                                                         random.randint(1, 28)),
                                                                     '%Y-%m-%d')
                        }
                        results.append(tweet_structure)
                    # else:
                    #     flag = False
                    #     break
            except BaseException as e:
                asyncio.sleep(60)
        else:
            with open('./api/collecting_data/data.json', 'r') as data_file:
                results = json.loads(data_file.read())
                for row in results:
                    row['created_at'] = datetime.datetime.strptime(row['created_at'],
                                                                   '%Y-%m-%d')

        return results, self.radius


if __name__ == '__main__':
    collector = TwitterCollector(center=[50.45, 30.56], radius=50)
    collector.search_last_days()
