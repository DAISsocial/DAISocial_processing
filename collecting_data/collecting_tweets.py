from tweepy import Cursor
from config.twitter import tw_api
import datetime
import time
import json
import asyncio


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
        converted_string = "{},{},{}km".format(self.center[0],
                                               self.center[1], self.radius)
        # while len(results) < 9000 and self.radius < 6:

        try:
            for tweet in Cursor(tw_api.search,
                                rpp=100,
                                geocode=converted_string,
                                show_user=False,
                                result_type="recent",
                                include_entities=True,
                                lang="en").items(1000):  # Counts
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
            flag = True
            while flag:

                converted_string = "{},{},{}km".format(self.center[0],
                                                       self.center[1], self.radius)
                try:
                    for tweet in Cursor(tw_api.search,
                                        rpp=100,
                                        geocode=converted_string,
                                        show_user=False,
                                        result_type="recent",
                                        include_entities=True,
                                        # lang="en"
                                        ).items(10000):  # Count

                        days_delta = (datetime.datetime.now() - tweet.created_at).days

                        if days_delta < days_count:
                            if tweet.coordinates:

                                tweet_structure = {
                                    'text': tweet.text,
                                    'coordinates': tweet.coordinates,
                                    'likes': tweet.favorite_count + 1,
                                    'retweets': tweet.retweet_count + 1,
                                    'created_at': tweet.created_at
                                }
                                results.append(tweet_structure)
                        else:
                            flag = False
                            break
                except BaseException as e:
                    asyncio.sleep(60)
        else:
            with open('data.json', 'r') as data_file:
                results = json.load(data_file)

        return results, self.radius


if __name__ == '__main__':
    collector = TwitterCollector(center=[50.45, 30.56], radius=50)
    collector.search_last_days()
