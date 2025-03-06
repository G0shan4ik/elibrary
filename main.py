from asyncio import run

from e_lib.parser import ParsManager
from e_lib.mixins import read_txt_file


async def main():
    all_links: list[str] = await read_txt_file('./pars_links.txt')

    manager: ParsManager = ParsManager(
        pars_urls=all_links
    )
    await manager.run()


def start_dev():
    run(main())