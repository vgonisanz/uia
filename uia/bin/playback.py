"""
Pay a macro to your keyboard and mouse
"""
import time
import typer

from uia.utils import setup_logger
from uia.core import Core

import structlog


logger = structlog.get_logger(__file__)


def main():
    typer.echo(f"Running {__file__}")

    core = Core()
    core.start_recording()
    time.sleep(3)
    core.start_playback()
    #core.run()


if __name__ == "__main__":
    setup_logger()
    typer.run(main)
