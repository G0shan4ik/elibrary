import diskcache
from loguru import logger


cache = diskcache.Cache('e_lib_cache')


def check_cache(value: str, key: str|None = None) -> bool:
    """
    :param value: html link pages
    :param key: link
    :return: bool
    """
    if key in cache:
        logger.warning(f'THIS key already exists ({key})')
        return False

    if key is None:
        return True

    cache[key] = value
    logger.success(f'Set key ({key})')
    return True