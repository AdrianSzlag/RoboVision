import json
import threading
from pathlib import Path


class Config:
    def __init__(self):
        self._lock = threading.Lock()
        self.config = dict()

    def save(self, filename):
        self._lock.acquire()
        json.dump(self.config, open(filename, 'w'))
        self._lock.release()

    def getValue(self, name, default):
        self._lock.acquire()
        if name not in self.config.keys():
            self.config[name] = default
        copy = self.config[name]
        self._lock.release()
        return copy

    def setValue(self, name, value):
        self._lock.acquire()
        self.config[name] = value
        self._lock.release()

    def load(self, filename):
        self._lock.acquire()
        self.config = json.load(open(Path(filename)))
        self._lock.release()
        return self
