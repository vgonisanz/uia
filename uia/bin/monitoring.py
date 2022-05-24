"""
Monitor your keyboard and mouse, printing the inputs in the stdout
"""
import typer

from uia.utils import setup_logger
from uia.core import Core

import structlog


logger = structlog.get_logger(__file__)


def on_scroll(x, y, dx, dy):
    logger.info("on_scroll", x=x, y=y, dx=dx, dy=dy)


def on_press(key):
    logger.info("on_press", key=key)


def on_release(key):
    logger.info("on_press", key=key)


def on_move(x, y):
    logger.info("on_move", x=x, y=y)


def on_click(x, y, button, pressed):
    logger.info("on_click", x=x, y=y, button=button, pressed=pressed)


def main():
    typer.echo(f"Running {__file__}")

    core = Core()
    core.set_mouse_callbacks(on_scroll, on_press, on_release)
    core.set_keyboard_callbacks(on_move, on_click)
    core.run()


if __name__ == "__main__":
    setup_logger()
    typer.run(main)
