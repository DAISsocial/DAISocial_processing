import gridfs
from config.database import db


def save_file(file, user_id):
    fs = gridfs.GridFS(db)

    file_id = fs.put(file, filename="File1")
    db.users.update_one({'_id': user_id},
                        {'$push': {'reports_ids': file_id}})

