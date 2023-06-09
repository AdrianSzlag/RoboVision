from threading import Thread, Lock
from settings import Config
import time
import serial
from pydantic import BaseModel

class Directions(BaseModel):
    forward: bool = False
    backward: bool = False
    left: bool = False
    right: bool = False
    
    def __eq__(self, other):
        if other == None:
            return False
        return self.left == other.left and self.forward == other.forward and self.backward == other.backward and self.right == other.right
    def isStatic(self):
        return self.left == False and self.forward == False and self.backward == False and self.right == False


class SerialControler:
    def __init__(self, port = '/dev/ttyUSB0'):
        self._port = port
        self._serial = serial.Serial(self._port)
        self._last: Directions = None
        self._instructions: Directions = None
        self._mutex = Lock()
        self._wait = Lock()

    def start(self):
        self._wait.acquire()
        t = Thread(target=self._update, args=())
        t.daemon = True
        t.name = 'Controller'
        t.start()
        return self

    def _update(self):
        while True:
            self._wait.acquire()
            with self._mutex:
                item = self._instructions
            if item == self._last:
                continue
            self._last = item
            #print(item)
            if item.forward == True:
                left = 1.
                right = 1.
            elif item.backward == True:
                left = -1.
                right = -1.
            else:
                left = 0.
                right = 0.
            if item.left == True:
                left -= 1.
                right += 1.
            elif item.right == True:
                left += 1.
                right -= 1.
            instructions = f'{left:.3f};{right:.3f}\n'
            #print(instructions)
            self._serial.write(bytes(instructions, 'utf-8'))
            time.sleep(1/25)
            
    def write(self, item: Directions):
        with self._mutex:
            self._instructions = item
        if self._wait.locked() == True:
            self._wait.release()
