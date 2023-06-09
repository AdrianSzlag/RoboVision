import cv2
from threading import Thread, Lock
from pydantic import BaseModel
from fps import FpsCounter
from controller import Directions
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import time


_app = FastAPI()
_fps = FpsCounter()
_wait = Lock()
_frameLock = Lock()
_frame: cv2.Mat = None


class Controll(BaseModel):
    controll: str = ""


def pushFrame(frame):
    with _frameLock:
        global _frame
        _frame = frame
    if _wait.locked() == True:
        _wait.release()


def getFps():
    return _fps.get()


def init(steeringCallback, changeControllCallback, log_level = 'warning', port = 5000):
    global _port, _log_level, _steeringCallback, _changeControllCallback
    _port = port
    _log_level = log_level
    _steeringCallback = steeringCallback
    _changeControllCallback = changeControllCallback
    _wait.acquire()


def _start():
    print(f'Web server running on: http://0.0.0.0:{_port}')
    uvicorn.run("fastweb:_app", host="0.0.0.0", log_level=_log_level,
                port=_port)


def start():
    t = Thread(target=_start, args=())
    t.name = 'Web_Server'
    t.daemon = True
    t.start()


def _gen():
    while True:
        _wait.acquire()
        start = time.time()
        with _frameLock:
            frame = _frame
        _fps.update()
        frame = cv2.resize(frame, (int(
            frame.shape[1]/2), int(frame.shape[0]/2)), interpolation=cv2.INTER_AREA)
        data = cv2.imencode(
            '.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 75])[1]
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(data) + b'\r\n')
        end = time.time()
        wait_time = 1/26 - (end - start)
        if wait_time < 0:
            wait_time = 0
        time.sleep(wait_time)


@_app.get('/video_feed')
def video_feed():
    return StreamingResponse(_gen(), media_type="multipart/x-mixed-replace;boundary=frame")


@_app.post('/directions')
def directions(item: Directions):
    return _steeringCallback(item)


@_app.post('/controll')
def directions(item: Controll):
    return _changeControllCallback(item)


_app.mount("/", StaticFiles(directory="templates", html=True), name="static")
