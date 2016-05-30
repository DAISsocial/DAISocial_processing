import json
from tweepy import Cursor
from config.twitter import tw_api
import datetime
import time
import json
import asyncio

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
                                ).items(10000):  # Count
                days_delta = (datetime.datetime.now() - tweet.created_at).days

                if days_delta < days_count:
                    if tweet.id not in results_ids:
                        file = open('./data.txt', 'a')
                        tweet_structure = {
                            'text': tweet.text,
                            'likes': tweet.favorite_count + 1,
                            'retweets': tweet.retweet_count + 1,
                            'created_at': str(tweet.created_at)
                        }
                        results_ids.add(tweet.id)
                        file.write(json.dumps(tweet_structure) + '\n')
                        file.close()
                else:
                    flag = False
                    break
        except Exception as e:
            time.sleep(20)

def process_file_to_right_format():
    with open('./data.txt') as file:


if __name__ == '__main__':
    collect_tweets_to_file()
    process_file_to_right_format()


