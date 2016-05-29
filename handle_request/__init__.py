from config.database import db
from analysis.sentiment.sentiment_analysis import MediaClassifier
from .check_location import Checker
from .search_location import Searcher


def save_request(user_id: int, data: dict):
    center = data.get('center')
    request_type = db.request_types.find_one()  # {'_id': data.get('type')})
    db.check_request.insert_one({'user_id': user_id,
                                 'location': {'type': 'Point', 'coordinates': center},
                                 'request_types': request_type})
    return request_type


def start_checking(user_id: int, data: dict):
    # SHOULD save_request(user_id, data)

    fake_data = {'center': [28.106518, -80.627753],
                 'radius': 2, 'type': 1}
    request_type = save_request(1, fake_data)
    classifier = MediaClassifier(data=fake_data,
                                 request_type=request_type)

    Checker(classifier=classifier)


def stat_searching(user_id: int, data: dict):
    # SHOULD save_request(user_id, data)

    fake_data = {'center': [28.106518, -80.627753],
                 'radius': 2, 'type': "57461d7546fd6e49ea000001"}
    request_type = save_request(1, fake_data)
    classifier = MediaClassifier(data=fake_data,
                                 request_type=request_type)

    Searcher(classifier=classifier)
