from pydantic import BaseModel
import typing
from pynput import mouse
from pynput import keyboard


class Move(BaseModel):
    x: int = 0
    y: int = 0


class Click(BaseModel):
    button: mouse.Button = mouse.Button.left
    pressed: bool = False
    x: int = 0
    y: int = 0


class Scroll(BaseModel):
    dx: int = 0
    dy: int = 0
    x: int = 0
    y: int = 0


class Key(BaseModel):
    """
    Probably a better way to manage keys in a general way
    """
    key: keyboard._xorg.KeyCode = keyboard.KeyCode.from_char("a")   # Only linux tested
    pressed: bool = False

    class Config:
        arbitrary_types_allowed = True
