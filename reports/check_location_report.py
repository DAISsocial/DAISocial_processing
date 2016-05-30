from .report_generator import ReportGenerator
from docx.shared import Inches


class CheckReport(ReportGenerator):

    def __init__(self):
        super().__init__()

    def create(self, graphic, last_common_media: dict, competitor_media):
        self.document.add_heading('Reporting Document', 0)

        p = self.document.add_paragraph('Last media keywords')
        p.add_run('bold').bold = True
        p.add_run('Most common words that appears together')
        for word in last_common_media.get('terms_max'):
            p.add_run(str(word))
        p.add_run('Most common words')
        for word in last_common_media.get('most_common'):
            p.add_run(str(word))

        self.document.add_page_break()

        self.document.add_heading('All media graphic by time.', level=1)
        self.document.add_picture('plots/plot.png')
        self.document.add_page_break()

        self.document.add_heading('Competitor media', level=1)
        p.add_run('bold').bold = True
        if competitor_media:
            for key, value in competitor_media:
                p.add_run('{} - Summary value: {}'.format(key, value))
        p.add_run(' and some ')
        p.add_run('italic.').italic = True

        self.document.save('docs/demo.docx')
