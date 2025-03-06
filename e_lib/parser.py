import asyncio
from typing import Optional, Awaitable
from loguru import logger

from playwright.async_api import async_playwright, Page
from random import randint

from .user_agents import user_agents
from .cache_core import check_cache
from .captcha_mixin import CaptchaMixin
from .mixins import async_write_csv


class ParsManager(CaptchaMixin):
    def __init__(self, pars_urls: list):
        self.pars_urls: list = pars_urls
        self.base_url: str = "https://elibrary.ru"
        self.session: Optional[Page] = None

        CaptchaMixin.__init__(self)

    @staticmethod
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    async def init_session(self) -> None:
        async with async_playwright() as p:
            logger.success('Start session')

            browser = await p.chromium.launch()
            context = await browser.new_context(
                viewport={
                    'width': 1920,
                    'height': 1080
                },
                user_agent=user_agents[randint(0, len(user_agents))],
                base_url=self.base_url,

            )
            self.session = await context.new_page()
            await self.session.goto(url=self.base_url, wait_until='commit')

            logger.success('Create context')

    async def pars_data(self, link: str):
        logger.info(f'Start pars link - {link}')
        response = await self.session.request.get(
            url=link
        )

        # _html: str = await response.text()
        # check_cache(
        #     value=_html,
        #     key=link
        # )
        # data = Спаршенные данные
        # await async_write_csv(data, 'FILE_NAME')

    async def run(self):
        logger.info("Start pars ...\n\n")

        await self.init_session()

        for links in self.chunks(self.pars_urls, 1):
            processes: [Awaitable] = [
                self.pars_data(link)
                for link in links
                if check_cache(value=link)
            ]

            await asyncio.gather(*processes)

            await asyncio.sleep(1000)
