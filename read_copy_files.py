import argparse
import asyncio

from aiopath import AsyncPath
from aioshutil import copyfile

from logger import logger


async def copy_file(source_file: AsyncPath, target_dir: AsyncPath):
    """Copies a file to a destination subdirectory based on the file extension."""
    try:
        file_extension = source_file.suffix.lower()
        extension_dir = target_dir / file_extension.strip(".")
        await extension_dir.mkdir(parents=True, exist_ok=True)

        destination_file = extension_dir / source_file.name
        await copyfile(source_file, destination_file)
        logger.info(f"File {source_file.name} is copied to {extension_dir}")
    except Exception as error:
        logger.error(f"Copy file error {source_file} to {extension_dir}: {error}")


async def read_dir(source_dir: AsyncPath, target_dir: AsyncPath):
    """Asynchronously traverses the source directory and
    copies files to the desired destination subdirectories."""
    tasks = []
    async for item in source_dir.rglob("*"):
        if await item.is_file():
            tasks.append(copy_file(item, target_dir))
    await asyncio.gather(*tasks)


def parse_arguments():
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(
        description="Asynchronous copying and file organization by extension."
    )
    parser.add_argument("source", help="Source directory.")
    parser.add_argument("destination", help="Destination directory.")
    return parser.parse_args()


def main():
    args = parse_arguments()
    source_dir = AsyncPath(args.source)
    target_dir = AsyncPath(args.destination)
    asyncio.run(read_dir(source_dir, target_dir))


if __name__ == "__main__":
    main()
