from .base import MediaClassifier


class LastMediaClassifier(MediaClassifier):

    def __init__(self, data):

        super().__init__(data)


def last_media_process(data: dict):
    my_clsf = LastMediaClassifier(data)
    most_common = my_clsf.get_terms()
