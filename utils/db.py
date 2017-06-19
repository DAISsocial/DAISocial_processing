from config import GLOBAL_CONFIG
from bson.objectid import ObjectId


def save_request_and_return_request_type(
        user_id: int, data: dict, type):
    db = GLOBAL_CONFIG.db
    center = data.get('center')
    # TODO: add here finding by request type
    request_type = db.request_types.find_one(
        ObjectId(data.get('request_type'))
    )
    if type is 'search':
        db.search_request.insert_one(
            {'user_id': ObjectId(user_id),
             'location': {'type': 'Point', 'coordinates': center},
             'request_types': request_type}
        )
    else:
        db.check_request.insert_one(
            {'user_id': ObjectId(user_id),
             'location': {'type': 'Point', 'coordinates': center},
             'request_types': request_type}
        )

    return request_type
