import sys
import json
import structlog

from pydantic import BaseModel, create_model

from pynput import mouse
from pynput import keyboard
from pydantic.json import pydantic_encoder
from uia.entities import Event


logger = structlog.get_logger(__file__)


class Session():
    """
    Keyboard and mouse session.
    It can be used to record and play keys press and mouse movement.
    """
    def __init__(self):
        self._last_record_events = []
        self._mcontroller = mouse.Controller()
        self._kcontroller = keyboard.Controller()
    
    def append(self, element):
        name = element.__class__.__name__

        logger.debug("session_append", name=name)

        event = Event(name=name,
                      value=element)
        self._last_record_events.append(event)
   
    def run(self):
        for event in self._last_record_events:
            logger.debug("run_event", **event.dict())
            self._mcontroller.click(event.value.button)


    def clear(self):
        self._last_record_events.clear()

    def export_to_file(self, filename):
        """
        Export the current session to a file
        """
        with open(filename, 'w') as f:
            json.dump(self._last_record_events, f,
                      indent=4, sort_keys=False, default=pydantic_encoder)   
    
    def import_from_file(self, filename):
        """
        Import a session from a file
        """
        self.clear()
        with open(filename, 'r') as f:
            json_data = json.load(f)
            for item in json_data:
                class_name = item['name']
                model_class = getattr(sys.modules["uia.entities"], class_name, None)
                if model_class:
                    instance = model_class(**item['value'])
                    event = Event(name=class_name, value=instance)
                    self._last_record_events.append(event)
                else:
                    logger.warning("model_class_not_recognized", class_name=class_name)
        logger.info("imported_session", len=len(self._last_record_events))
        