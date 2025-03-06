import aiofiles


async def read_txt_file(file_path: str) -> list[str]:
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
        content = await file.read()

        return [
            line.strip()
            for line in content.split('\n')
            if line.strip()
        ]


async def async_write_csv(data: list, file_path: str) -> None:
    async with aiofiles.open(file_path, mode="a", encoding='utf-8') as f:
        await f.write(f"{', '.join(data)}\n")


