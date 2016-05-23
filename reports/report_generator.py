import gridfs
from config.database import db
from docx import Document


class ReportGenerator:

    def __init__(self):
        self.file = None
        self.user_id = None
        self.document = Document()

    def save(self):
        fs = gridfs.GridFS(db)

        file_id = fs.put(self.file, filename="File1")
        db.users.update_one({'_id': self.user_id},
                            {'$push': {'reports_ids': file_id}})
