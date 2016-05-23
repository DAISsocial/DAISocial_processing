from config.foursquare import client


class FoursquareCollector:

    def __init__(self, center, radius=None, count=None):
        self.center = center
        self.radius = radius
        self.count = count

    def use(self):
        _client = client

