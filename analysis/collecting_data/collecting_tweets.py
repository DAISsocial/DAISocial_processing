from tweepy import Cursor
from config.twitter import tw_api


class TwitterCollector:

    def __init__(self, center, radius=None, count=None):
        self.center = center
        self.radius = radius
        self.count = count

    def search(self):

        if not self.radius:
            radius = 2

        results = set()
        while len(results) < 9000 and radius < 6:

            converted_string = "{},{},{}km".format(self.center[0], self.center[1], radius)

            for tweet in Cursor(tw_api.search,
                                rpp=100,
                                geocode=converted_string,
                                show_user=False,
                                result_type="recent",
                                include_entities=True,
                                lang="en").items(10000):  # Counts
                results.add(tweet)

        # NEED to be processed tweet.favorited_count+1 ,tweet.retweeted_count+1
        return results, radius

    def search_last_month(self):

        pass
