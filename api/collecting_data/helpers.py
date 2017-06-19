import datetime
import json
import random
import time

from tweepy import Cursor

from config import GLOBAL_CONFIG


def collect_tweets_to_file(days_count):
    results_ids = set()
    flag = True
    file = open('./data.json', 'a')
    while flag:
        twitter_client = GLOBAL_CONFIG.twitter_client
        try:
            for tweet in Cursor(
                twitter_client.search,
                q='food',
                rpp=100,
                # geocode=converted_string,
                show_user=False,
                # result_type="recent",
                include_entities=True,
                lang="en"
            ).items(10000):  # Count
                days_delta = (datetime.datetime.now() - tweet.created_at).days

                if days_delta < days_count:
                    if tweet.id not in results_ids:
                        tweet_structure = {
                            'text': tweet.text,
                            'likes': tweet.favorite_count + 1,
                            'retweets': tweet.retweet_count + 1,
                            'created_at': str(tweet.created_at)
                        }
                        results_ids.add(tweet.id)
                        file.write(json.dumps(tweet_structure) + ',\n')

                else:
                    flag = False
                    break
        except Exception as e:
            time.sleep(20)

    file.close()


def process_file_to_right_format():
    file_output = open('./data.json', 'a')
    with open('./data.json') as file:
        data = json.loads(file.read())
        for row in data:
            row['coordinates'] = [random.uniform(28.108610, 28.113385),
                                  random.uniform(-80.617204, -80.634789)]

            row['created_at'] = "2017-{}-{}".format(random.randint(2, 5),
                                                    random.randint(1, 28))
            file_output.write(json.dumps(row) + ", \n")
    file_output.close()
