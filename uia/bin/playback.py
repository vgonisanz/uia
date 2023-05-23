"""
Play a macro to your keyboard and mouse
"""
import time
import typer

from uia.utils import setup_logger
from uia.core import Core

import structlog


logger = structlog.get_logger(__file__)


def main(filename: str = "session.json"):
    typer.echo(f"Running {__file__}")

    core = Core()
    core.import_session(filename)
    core.start_playback()


if __name__ == "__main__":
    setup_logger()
    typer.run(main)
