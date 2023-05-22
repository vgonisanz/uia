import json
import structlog

from pydantic import BaseModel
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
    
    def append(self, element):
        name = element.__class__.__name__

        logger.debug("session_append", name=name)

        event = Event(name=name,
                      value=element)
        logger.debug("element", **element.dict())
        logger.debug("event", **event.dict())
        self._last_record_events.append(event)
   
    def clear(self):
        self._last_record_events.clear()

    def export_to_file(self, filename):
        """
        Export the current session to a file
        """
        with open(filename, 'w') as f:
            json.dump(self._last_record_events, f,
                      indent=4, sort_keys=False, default=pydantic_encoder)   
    
    def import_to_file(self, filename):
        """
        Import a session from a file
        """
        #Something like this to create from text-scratch objects
        #class_name = element.__class__.__name__
        #model_class = type(class_name, (BaseModel,), element.dict())
        with open(filename, 'r') as f:
            data = json.load(f)
        