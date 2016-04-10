import asyncio
from aiohttp import web
import urllib3


class ProcessingServer:

    def __init__(self):
        self.app = web.Application()


if __name__ == '__main__':
    my_server = ProcessingServer()
