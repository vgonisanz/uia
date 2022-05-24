"""
Core of the project to manage all Input devices
"""
import structlog


from pynput import mouse
from pynput import keyboard


logger = structlog.get_logger(__file__)


class Core():
    """
    Main class to control mouse & keyboard
    """
    def __init__(self):
        self._callback_on_scroll = None
        self._callback_on_press = None
        self._callback_on_release = None

        self._callback_on_move = None
        self._callback_on_click = None

        self._mlistener = mouse.Listener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll
        )

        self._klistener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        
        self._mlistener.start()
        self._klistener.start()

    def set_mouse_callbacks(self, on_scroll=None, on_press=None, on_release=None):
        self._callback_on_scroll = on_scroll
        self._callback_on_press = on_press
        self._callback_on_release = on_release

    def set_keyboard_callbacks(self, on_move=None, on_click=None):
        self._callback_on_move = on_move
        self._callback_on_click = on_click

    def _on_move(self, x, y):
        logger.debug("on_move", x=x, y=y)
        if self._callback_on_move:
            self._callback_on_move(x=x, y=y)

    def _on_click(self, x, y, button, pressed):
        logger.debug("on_click", x=x, y=y, button=button, pressed=pressed)
        if self._callback_on_click:
            self._callback_on_click(x=x, y=y, button=button, pressed=pressed)

    def _on_scroll(self, x, y, dx, dy):
        logger.debug("on_scroll", x=x, y=y, dx=dx, dy=dy)
        if self._callback_on_scroll:
            self._callback_on_scroll(x=x, y=y, dx=dx, dy=dy)

    def _on_press(self, key):
        logger.debug("on_press", key=key)
        if self._callback_on_press:
            self._callback_on_press(key=key)

    def _on_release(self, key):
        logger.debug("on_press", key=key)
        if self._callback_on_release:
            self._callback_on_release(key=key)
    
    def run(self):
        while True:
            pass