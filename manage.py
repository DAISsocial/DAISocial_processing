from manager import Manager

from api.collecting_data.helpers import (
    collect_tweets_to_file,
    process_file_to_right_format
)
from server import ProcessingServer

manager = Manager()


@manager.command
def runserver():
    ProcessingServer().run()

if __name__ == '__main__':
    days_count = 120
    process_file_to_right_format()
