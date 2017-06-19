from .views import SearchView
from .views import CheckView


routes = [
    ('POST', '/users/{id}/search_request', SearchView),
    ('POST', '/users/{id}/check_request',  CheckView)
]
