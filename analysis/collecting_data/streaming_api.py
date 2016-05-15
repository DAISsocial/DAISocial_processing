from tweepy import Stream
from tweepy.streaming import StreamListener
from config.twitter import auth


class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


def create_stream_listener():
    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(track=['python'], async=True)


if __name__ == '__main__':
    create_stream_listener()
