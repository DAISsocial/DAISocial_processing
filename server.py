import asyncio
from aiohttp import web


class ProcessingServer:

    def __init__(self):
        self.app = web.Application()
        self.app.router.add_route('GET', '/users/{id}/search_request', self.search_handler)
        self.app.router.add_route('GET', '/users/{id}/check_request', self.check_handler)
        web.run_app(self.app)

    @asyncio.coroutine
    def search_handler(self, request):
        user_id = request.match_info.get('id')
        return web.Response(text="Hi, {}".format(user_id))

    @asyncio.coroutine
    def check_handler(self, request):
        return web.Response()

if __name__ == '__main__':
    my_server = ProcessingServer()
