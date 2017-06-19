import gridfs
from bson.objectid import ObjectId
from docx import Document

from config import GLOBAL_CONFIG


class ReportGenerator:

    def __init__(self, user_id):
        self.user_id = user_id
        self.document = Document()

    def save(self, filename):
        db = GLOBAL_CONFIG.db
        fs = gridfs.GridFS(db)

        file_id = fs.put(
            open(r'docs/{}'.format(filename), 'rb'),
            filename="demo.docx"  # TODO: RANDOM NAME
        )
        db.users.update_one(
            {'_id': ObjectId(self.user_id)},
            {'$push': {'reports_ids': file_id}}
        )
