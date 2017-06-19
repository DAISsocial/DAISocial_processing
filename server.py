from aiohttp import web

from api.routes import routes


class ProcessingServer:

    def __init__(self):
        self.app = web.Application()

        # adding routes to application
        for route in routes:
            self.app.router.add_route(*route)

    def run(self):
        web.run_app(self.app)

if __name__ == '__main__':
    ProcessingServer().run()
