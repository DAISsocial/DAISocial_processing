from config.database import db


def save_request(user_id: int, data: dict):
    center = data.get('center')
    request_type = db.request_type.find_one({'_id': data.get('type')})
    _id = db.check_request.insert_one({'user_id': user_id,
                                 'location': {'type': 'Point', 'coordinates': center},
                                 'request_types': request_type}).inserted_id
    print(_id)


def start(user_id: int, data: dict):
    # save_request(user_id, data)
    save_request(1, {'center': [30, 50], 'type': 1})
