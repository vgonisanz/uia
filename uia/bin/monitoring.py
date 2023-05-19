"""
Monitor your keyboard and mouse, printing the inputs in the stdout
"""
import typer

from uia.utils import setup_logger
from uia.core import Core

import structlog


logger = structlog.get_logger(__file__)


def on_scroll(scroll):
    logger.info("on_scroll", **scroll.dict())


def on_key(key):
    logger.info("on_key", **key.dict())


def on_move(move):
    logger.info("on_move", **move.dict())


def on_click(click):
    logger.info("on_click", **click.dict())


def main():
    typer.echo(f"Running {__file__}")

    core = Core()
    core.set_mouse_callbacks(on_scroll=on_scroll,
                             on_press=on_key,
                             on_release=on_key)
    core.set_keyboard_callbacks(on_move=on_move,
                                on_click=on_click)
    core.run()


if __name__ == "__main__":
    setup_logger()
    typer.run(main)
