import sys
import time
import json

from pydantic import BaseModel, create_model

from pynput import mouse
from pynput import keyboard
from pydantic.json import pydantic_encoder
from uia.entities import Event

import structlog

logger = structlog.get_logger(__file__)


class Session():
    """
    Keyboard and mouse session.
    It can be used to record and play keys press and mouse movement.
    """
    def __init__(self):
        self._events = []
        self._granularity = 3   # ms in timestamp by design
        self._recording = False
        self._start_timestamp = time.time()
        self._mcontroller = mouse.Controller()
        self._kcontroller = keyboard.Controller()

    def _calculate_relative_timestamp(self):
        return round(time.time() - self._start_timestamp, self._granularity)
  
    def start_recording(self):
        logger.info("start_record")
        self._recording = True
        self._start_timestamp = time.time()

    def stop_recording(self):
        logger.info("stop_record")
        self._recording = False

    def append(self, element):
        if not self._recording:
            return

        name = element.__class__.__name__

        logger.debug("session_append", name=name)

        event = Event(name=name,
                      value=element,
                      timestamp=self._calculate_relative_timestamp())
        self._events.append(event)
   
    def run(self):
        for event in self._events:
            logger.debug("run_event", **event.dict())
            if event.name == "Position":
                self._mcontroller.position = (event.value.x, event.value.y)
            if event.name == "Click":
                self._mcontroller.click(event.value.button)
            if event.name == "Scroll":
                self._mcontroller.scroll(event.value.dx, event.value.dy)
            if event.name == "Key":
                print("key_todo")


    def clear(self):
        logger.debug("clear_session")
        self._events.clear()

    def export_to_file(self, filename):
        """
        Export the current session to a file
        """
        with open(filename, 'w') as f:
            json.dump(self._events, f,
                      indent=4, sort_keys=False, default=pydantic_encoder)   
    
    def import_from_file(self, filename):
        """
        Import a session from a file
        """
        self.clear()
        with open(filename, 'r') as f:
            json_data = json.load(f)
            for item in json_data:
                self._append_model_if_exist(item['name'],
                                            item['value'],
                                            item['timestamp'])
        logger.info("imported_session", len=len(self._events))
    
    def _append_model_if_exist(self, class_name, value, timestamp):
        model_class = Session._deduce_model_from_str(class_name)
        if model_class:
            instance = model_class(**value)
            event = Event(name=class_name, value=instance, timestamp=timestamp)
            self._events.append(event)
        else:
            logger.warning("model_class_not_recognized", class_name=class_name)
    
    @staticmethod
    def _deduce_model_from_str(class_name):
        """
        Given a string, try to create a model from entities.
        If string is not recognized, return None
        """
        return getattr(sys.modules["uia.entities"], class_name, None)