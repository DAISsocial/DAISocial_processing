import gridfs
from config.database import db
from docx import Document


class ReportGenerator:

    def __init__(self):
        self.user_id = None
        self.document = Document()

    def save(self, filename):
        fs = gridfs.GridFS(db)

        file_id = fs.put(open('docs/{}'.format(filename)).read().decode('utf8'), filename="demo.docx")
        db.users.update_one({'_id': self.user_id},
                            {'$push': {'reports_ids': file_id}})
