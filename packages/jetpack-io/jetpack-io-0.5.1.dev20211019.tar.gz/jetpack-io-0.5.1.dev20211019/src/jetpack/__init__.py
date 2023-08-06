__version__ = "0.5.1-dev20211019"

from jetpack._job.interface import job
from jetpack._remote.interface import remote
from jetpack.cli import handle as init
from jetpack.cmd import root
from jetpack.redis import redis


def run() -> None:
    root.cli()
