"""Reading config from config.ini file and setting global config for """
import configparser
import collections

import foursquare
import tweepy
import pymongo


def read_config():

    ScriptConfig = collections.namedtuple(
        'Config', ['db', 'twitter_client', 'foursquare_client', 'cached_mode']
    )

    config = configparser.ConfigParser()
    config.read('config.ini')

    # Initialize db client
    db_config = config['mongodb']
    mongo_client = pymongo.MongoClient(
        'mongodb://{}:{}:{}/{}'.format(
            db_config['user'], db_config['host'],
            db_config['port'], db_config['database']
        )
    )
    db = mongo_client['daisocial']

    # Initialize twitter client
    twitter_auth = tweepy.OAuthHandler(
        consumer_key='sSFfCnVNQlwYZsvzd12K1DpM5',
        consumer_secret='xTLzC4jCOfHLWU26Qarqi2orV1rpyRZ1H95Qsm1JeVooz3dhns'
    )
    twitter_auth.set_access_token('4058691645-I1Yqe21bjabJS5yj1FIQPVX4BV1nDqYnVZxViwn',
                                  'RAW6vI2nsHkGaF6ks4wIalx4TR4m39wxa5HApDQAoShu1')
    twitter_api_client = tweepy.API(
        twitter_auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True
    )

    # Initialize foursquare client
    foursquare_api_client = foursquare.Foursquare(
        client_id='25M3NFZRXPTMY5TVWCC5YK0UX51BOLX1UWJOPCJCOAPTNMHE',
        client_secret='LHXCE0KUXBHLOD4IU5L3R5TWZHAZFP1ELACEHGNQMTO3LZE2',
        version='20120609'
    )

    # Mode
    cached_mode = config.getboolean('other', 'cached_mode')

    return ScriptConfig(
        db=db,
        twitter_client=twitter_api_client,
        foursquare_client=foursquare_api_client,
        cached_mode=cached_mode
    )

GLOBAL_CONFIG = read_config()
