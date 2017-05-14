from aiohttp import web

from config import GLOBAL_CONFIG


def token_required(f):

    def wrapper(self, request):
        db = GLOBAL_CONFIG.db

        secret_token = request.match_info.get('secret_token')
        if db.users.find_one(
            {'_id': request.match_info.get('_id')}
        ).get('secret_token') == secret_token:
            f(self, request)
        else:
            web.Response(text="Sorry wrong user token was given...")

    return wrapper
