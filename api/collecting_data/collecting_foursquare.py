from config import GLOBAL_CONFIG


class FoursquareCollector:

    def __init__(self, center, radius=None, count=None):
        self.center = center
        self.radius = radius
        self.count = count

    def use(self):
        _client = GLOBAL_CONFIG.foursquare_client

