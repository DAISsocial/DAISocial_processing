import asyncio
import logging

from aiohttp import web

from api.handle_request import (
    start_checking, start_searching
)


class ProcessingServer:

    def __init__(self):
        self.app = web.Application()
        self.app.router.add_route('POST', '/users/{id}/search_request', self.search_handler)
        self.app.router.add_route('POST', '/users/{id}/check_request', self.check_handler)

    @asyncio.coroutine
    def search_handler(self, request):
        user_id = request.match_info.get('id')

        if request.has_body:
            data = yield from request.json()
            logging.debug(data)
            start_searching(user_id, data)

        return web.Response(text="Well done, {},now you can check your results"
                            .format(user_id))

    @asyncio.coroutine
    def check_handler(self, request):
        user_id = request.match_info.get('id')

        if request.has_body:
            data = yield from request.json()
            logging.debug(data)
            start_checking(user_id, data)

        return web.Response(text="Well done, {},now you can check your results"
                            .format(user_id))

    def run(self):
        web.run_app(self.app)

if __name__ == '__main__':
    ProcessingServer().run()
