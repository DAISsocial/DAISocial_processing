from aiohttp import web

from config.logger import logger
from utils.db import save_request_and_return_request_type

from ..analysis.sentiment import MediaClassifier
from ..managers import SearcherManager

from config import GLOBAL_CONFIG


class SearchView(web.View):

    async def post(self):
        user_id = self.request.match_info.get('id')

        if self.request.has_body:
            data = await self.request.json()
            logger.info(data)
            if GLOBAL_CONFIG.cached_mode:
                data = {'center': [28.106518, -80.627753],
                        'radius': 2, 'request_type': '574dd13046fd6e0eed000001'}
            request_type = save_request_and_return_request_type(
                user_id=user_id,
                data=data,
                type='search'
            )
            classifier = MediaClassifier(
                data=data, request_type=request_type
            )

            SearcherManager(
                classifier=classifier,
                user_id=user_id
            ).run()

        logger.info('Finished')
        return web.Response(
            text="Well done, {},now you can check your results"
                  .format(user_id)
        )
