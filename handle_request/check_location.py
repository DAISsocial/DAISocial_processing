from analysis.sentiment.sentiment_analysis import MediaClassifier


class Checker:

    def __init__(self, classifier: MediaClassifier):
        self.classifier = classifier
        self.classifier.calculate_semantic_orientation()

    def all_media(self):
        pass

    def competitor_media(self):
        pass

    def last_media(self):
        pass
