import threading
import time

class FpsCounter:
    def __init__(self):
        self._mutex = threading.Lock()
        self._frames = 0
        self._start_time = time.time()
        self._fps = 0
    def update(self):
        self._frames += 1
        if time.time() - self._start_time >= 1:
            self._mutex.acquire()
            self._fps = self._frames
            self._mutex.release()
            self._start_time += 1
            self._frames = 0
    def get(self):
        self._mutex.acquire()
        i = self._fps
        self._mutex.release()
        return i
            