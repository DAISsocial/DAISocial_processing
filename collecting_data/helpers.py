import json
from tweepy import Cursor
from config.twitter import tw_api
import datetime
import time
import json
import asyncio
import random


def collect_tweets_to_file():
    radius = 2
    center = [28.106518, -80.627753]
    days_count = 120
    results_ids = set()
    flag = True
    while flag:
        converted_string = "{},{},{}km".format(center[0],
                                               center[1], radius)
        try:
            for tweet in Cursor(tw_api.search,
                                rpp=100,
                                geocode=converted_string,
                                show_user=False,
                                result_type="recent",
                                include_entities=True,
                                # lang="en"
                                ).items(1000):  # Count
                days_delta = (datetime.datetime.now() - tweet.created_at).days

                if days_delta < days_count:
                    if tweet.id not in results_ids:
                        file = open('./data.json', 'a')
                        tweet_structure = {
                            'text': tweet.text,
                            'likes': tweet.favorite_count + 1,
                            'retweets': tweet.retweet_count + 1,
                            'created_at': str(tweet.created_at)
                        }
                        results_ids.add(tweet.id)
                        file.write(json.dumps(tweet_structure) + ',\n')
                        file.close()
                else:
                    flag = False
                    break
        except Exception as e:
            time.sleep(20)


def process_file_to_right_format():
    file_output = open('data_converted.json', 'a')
    with open('./data.json') as file:
        data = json.loads(file.read())
        for row in data:
            row['coordinates'] = [random.uniform(28.108610, 28.113385),
                                  random.uniform(-80.617204, -80.634789)]

            row['created_at'] = "2016-{}-{}".format(random.randint(2, 5),
                                                    random.randint(1, 28))
            file_output.write(json.dumps(row) + ", \n")
    file_output.close()

if __name__ == '__main__':
    process_file_to_right_format()


