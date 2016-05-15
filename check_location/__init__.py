from config.database import db


def save_request(user_id: int, data: dict):
    center = data.get('center')
    request_type = db.request_type.find_one({'_id': data.get('type')})
    db.check_request.insert_one({'user_id': user_id,
                                 'location': {'type': 'Point', 'coordinates': center},
                                 'request_types': request_type})
    return request_type


def start(user_id: int, data: dict):
    # save_request(user_id, data)
    fake_data = {'center': [31.0, 52.0], 'radius': 50, 'type': 1}
    request_type = save_request(1, fake_data)


