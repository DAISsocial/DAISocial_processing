import asyncio
from aiohttp import web
from check_location import start as check_start


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
        return web.Response(text="Hi, {}".format(user_id))

    @asyncio.coroutine
    def check_handler(self, request):
        user_id = request.match_info.get('id')
        if request.has_body:
            data = yield from request.json()
            check_start(user_id, data)
        return web.Response(text="Hi, {}".format(user_id))

if __name__ == '__main__':
    my_server = ProcessingServer()
