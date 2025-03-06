import time

from twocaptcha import TwoCaptcha
from loguru import logger


__all__ = ["CaptchaMixin"]


API_KEY_RUCAPTCHA = ''


class CaptchaMixin:
    def __init__(self):
        if API_KEY_RUCAPTCHA is None:
            raise ValueError("No API_KEY_RUCAPTCHA")
        self._solver = TwoCaptcha(API_KEY_RUCAPTCHA)

    async def solve_captcha(self, key: str, page_url: str) -> bool:
        """
        Solves a captcha
        """
        _start_time = time.time()

        logger.info(f'Start solved CAPTCHA (key: {key})')
        try:
            solved_key = self._solver.solve_captcha(
                site_key=key,
                page_url=page_url,
            )
            if not solved_key:
                raise Exception('Artificial exclusion (The captcha has not been solved)')

            logger.success(f'Success solved captcha (time: {round(time.time() - _start_time, 2)} sec)')

        except Exception as ex:
            logger.error(f'The captcha has not been solved\n{ex}\n\n')
            return False

        logger.success(f'STATUS SOLVED CAPTCHA')
        return True
