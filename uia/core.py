"""
Core of the project to manage all Input devices
"""
import structlog


from uia.entities import (
    ButtonState,
    Position,
    Click,
    Scroll,
    Key
)
from uia.session import Session
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

        self._session = Session()

        self._mlistener = mouse.Listener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll
        )

        self._klistener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        
        logger.info("starting_devices")
        self._mlistener.start()
        self._klistener.start()

        self._mlistener.wait()
        self._klistener.wait()
        logger.info("devices_ready")

    def set_mouse_callbacks(self, on_scroll=None, on_press=None, on_release=None):
        self._callback_on_scroll = on_scroll
        self._callback_on_press = on_press
        self._callback_on_release = on_release

    def set_keyboard_callbacks(self, on_move=None, on_click=None):
        self._callback_on_move = on_move
        self._callback_on_click = on_click

    def _on_move(self, x, y):
        pos = Position(x=x, y=y)
        logger.debug("on_move", **pos.dict())
        if self._callback_on_move:
            self._callback_on_move(pos)
        self._session.append(pos)

    def _on_click(self, x, y, button, pressed):
        click = Click(position=Position(x=x, y=y),
                      button=button,
                      state=ButtonState(pressed))
        logger.debug("on_click", **click.dict())
        
        if self._callback_on_click:
            self._callback_on_click(click)
        
        self._session.append(click)

    def _on_scroll(self, x, y, dx, dy):
        scroll = Scroll(x=x, y=y, dx=dx, dy=dy)
        logger.debug("on_scroll", **scroll.dict())
        if self._callback_on_scroll:
            self._callback_on_scroll(scroll)

        self._session.append(scroll)

    def _on_press(self, keyid):
        key = Key(key=keyboard.KeyCode.from_char(keyid), pressed=True)
        logger.debug("on_press", **key.dict())
        if self._callback_on_press:
            self._callback_on_press(key=key)
        
        self._session.append(key)

    def _on_release(self, keyid):
        key = Key(key=keyboard.KeyCode.from_char(keyid), pressed=False)
        logger.debug("on_press", **key.dict())
        if self._callback_on_release:
            self._callback_on_release(key=key)
    
        self._session.append(key)
    

    def start_recording(self):
        self._session.start_recording()

    def stop_recording(self):
        self._session.stop_recording()

    def start_playback(self):
        logger.info("start_playback")
        self._session.start_playback()

    def stop_playback(self):
        logger.info("stop_playback")

    def import_session(self, filename: str = "session.json"):
        logger.info("import_session", filename=filename)
        self._session.import_from_file(filename)

    def export_session(self, filename: str = "session.json"):
        logger.info("export_session", filename=filename)
        self._session.export_to_file(filename)
