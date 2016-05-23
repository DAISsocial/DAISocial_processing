import asyncio
from aiohttp import web
from handle_request import (
    start_checking, stat_searching
)
import logging
from config.database import db


def token_required(f):

    def wrapper(self, request):

        secret_token = request.match_info.get('secret_token')
        if db.users.find_one({'_id': request.match_info.get('_id')})\
                .get('secret_token') == secret_token:
            f(self, request)
        else:
            web.Response(text="Sorry wrong user token was given...")

    return wrapper


class ProcessingServer:

    def __init__(self):
        self.app = web.Application()
        self.app.router.add_route('POST', '/users/{id}/search_request', self.search_handler)
        self.app.router.add_route('POST', '/users/{id}/check_request', self.check_handler)
        web.run_app(self.app)

    @asyncio.coroutine
    def search_handler(self, request):
        user_id = request.match_info.get('id')

        if request.has_body:
            data = yield from request.json()
            logging.debug(data)
            stat_searching(user_id, data)

        return web.Response(text="Hi, {}".format(user_id))

    @asyncio.coroutine
    def check_handler(self, request):
        user_id = request.match_info.get('id')

        if request.has_body:
            data = yield from request.json()
            logging.debug(data)
            start_checking(user_id, data)

        return web.Response(text="Hi, {}".format(user_id))

if __name__ == '__main__':
    my_server = ProcessingServer()
