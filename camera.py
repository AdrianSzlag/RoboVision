from threading import Lock
from concurrent.futures import ThreadPoolExecutor
import cv2
from fps import FpsCounter


class CameraFeed:
    def __init__(self, callback, video_source = 0, max_workers = 3):
        self._stream = cv2.VideoCapture(video_source)
        self._fps = FpsCounter()
        self._max_workers = max_workers
        self._numer_of_tasks = 0
        self._mutex = Lock()
        self._pool = ThreadPoolExecutor(self._max_workers+1)
        self._callback = callback


    def start(self):
        self._pool.submit(self._update)
        return self


    def _update(self):
        (grabbed, frame) = self._stream.read()
        self._pool.submit(self._update)
        with self._mutex:
            if self._numer_of_tasks > self._max_workers:
                return
            self._numer_of_tasks += 1
            self._fps.update()
        self._callback(frame)
        with self._mutex:
            self._numer_of_tasks -= 1


    def getFps(self):
        return self._fps.get()
