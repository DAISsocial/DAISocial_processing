from .report_generator import ReportGenerator


class SearchReport(ReportGenerator):

    def __init__(self, user_id):
        super().__init__(user_id)

    def create(self, best_cluster):
        self.document.add_heading('Reporting Document', 0)

        p = self.document.add_paragraph('')
        run = p.add_run('Best place for your business')
        run.bold = True
        run.add_break()
        run = p.add_run('Here is the best place')
        run.add_break()
        run = p.add_run('http://maps.google.com/?q={},{}'.format(best_cluster['center'][0],
                                                                 best_cluster['center'][1]))
        run.add_break()
        run = p.add_run(' it\'s center with founded radius {}'
                        .format(round(best_cluster['max_distance'])))
        run.add_break()
        p.add_run('We strongly recommend you not to searching place with given radius,\
                   cause it is maximal length, we recommend radius ~ '
                  .format(round(best_cluster['max_distance'] / 3.)))

        self.document.save('docs/demo1.docx')
