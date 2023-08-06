import click
import os
import sys

debug = True
# debug = os.environ.get('HI_DEBUG') or False
if not debug:
    sys.tracebacklimit = 0

@click.group()
def cli():
    pass

from hi.config import init
init()

from hi.apis import get_apis


def __build_cli(apis = []):
    for api in apis:
        for command in [getattr(api, a) for a in dir(api) if isinstance(getattr(api, a), click.core.Command)]:
            cli.add_command(command)

__build_cli(get_apis(debug))
