from config.database import db
from analysis import start_analysis


def save_request(user_id: int, data: dict):
    center = data.get('center')
    request_type = db.request_type.find_one({'_id': data.get('type')})
    db.check_request.insert_one({'user_id': user_id,
                                 'loc': center,
                                 'request_types': request_type})


def start(user_id: int, data: dict):
    # save_request(user_id, data)
    fake_data = {'center': [30, 50], 'type': 1}
    save_request(1, fake_data)
    start_analysis(fake_data)
