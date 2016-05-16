from analysis.sentiment.sentiment_analysis import MediaClassifier
from analysis.ordinary_list_squares.k_means_clustering import find_centers

data = {'center': [50.45, 30.56], 'radius': 50}

classifier = MediaClassifier(data=data, request_type=None)
tweets_with_so = classifier.calculate_summary_so()
