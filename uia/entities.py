import typing
from enum import Enum


from pydantic import BaseModel
from pynput import mouse
from pynput import keyboard


class ButtonState(Enum):
    RELEASED = 0
    PRESSED = 1

class Position(BaseModel):
    x: int
    y: int


class Click(BaseModel):
    position: Position = Position(x=0, y=0)
    button: mouse.Button = mouse.Button.left
    state: ButtonState = ButtonState.RELEASED


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


class Event(BaseModel):
    name: str
    value: typing.Union["Position", "Click", "Scroll", "Key"]
 