import asyncio
import logging
from pathlib import Path

import click

import locapip


@click.command()
@click.option('--port', type=int, default=6547)
@click.option('--proto', type=click.Path(file_okay=False, dir_okay=True, path_type=Path), multiple=True)
def main(port: int, proto):
    print(f'{locapip.name} {locapip.version}')
    print(f'--port  {port}')

    if proto is not None:
        for path in proto:
            locapip.import_package(path)

    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(locapip.serve(port))


if __name__ == "__main__":
    main()
