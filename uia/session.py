import json
from uia.entities import Event


class Session():
    """
    Keyboard and mouse session.
    It can be used to record and play keys press and mouse movement.
    """
    def __init__(self):
        self._last_record_events = []
    
    def append(self, element):
        event = Event(type=str(type(element)), value=element)
        print(event)
        self._last_record_events.append(event)
    
    def clear(self):
        self._last_record_events.clear()

    def export_to_file(self, filename):
        """
        Export the current session to a file
        """
        with open(filename, 'w') as f:
            for event in self._last_record_events:
                json.dump(event.json(), f)
    
    def import_to_file(self, filename):
        """
        Import a session from a file
        """
        with open(filename, 'r') as f:
            data = json.load(f)
        