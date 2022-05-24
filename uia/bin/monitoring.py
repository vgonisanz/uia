"""
Monitor your keyboard and mouse, printing the inputs in the stdout
"""
import typer

from uia.utils import setup_logger
import structlog

from pynput import mouse
from pynput import keyboard


logger = structlog.get_logger(__file__)


def on_move(x, y):
    logger.info("on_move", x=x, y=y)


def on_click(x, y, button, pressed):
    logger.info("on_click", x=x, y=y, button=button, pressed=pressed)


def on_scroll(x, y, dx, dy):
    logger.info("on_scroll", x=x, y=y, dx=dx, dy=dy)


def on_press(key):
    logger.info("on_press", key=key)


def on_release(key):
    logger.info("on_press", key=key)


def main():
    typer.echo(f"Running {__file__}")

    mlistener = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll
    )

    klistener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    )
    
    mlistener.start()
    klistener.start()

    while True:
        pass


if __name__ == "__main__":
    setup_logger()
    typer.run(main)
