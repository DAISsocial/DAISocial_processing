from .report_generator import ReportGenerator
from docx.shared import Inches


class CheckReport(ReportGenerator):

    def __init__(self):
        super().__init__()

    def create(self):
        self.document.add_heading('Reporting Document', 0)

        p = self.document.add_paragraph('A plain paragraph having some ')
        p.add_run('bold').bold = True
        p.add_run(' and some ')
        p.add_run('italic.').italic = True

        self.document.add_heading('Heading, level 1', level=1)

        self.document.add_picture('monty-truth.png', width=Inches(1.25))

        self.document.add_page_break()

        self.document.save('demo.docx')

