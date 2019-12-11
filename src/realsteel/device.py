from multiprocessing import Pool, Process, Queue
import time
import serial
from realsteel.robot import ArmJoints


class DEVICE:
    def __init__(self, *args, **kwargs):
        pass


class ROBOT_DEVICE(DEVICE):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ser = serial.Serial('/dev/ttyUSB0', baudrate=115200)
        self.ser = ser
        self.running = False

    def launch(self, queue: Queue):
        q = queue
        p = Process(target=self.main_loop, args=(q,))
        self.running = True
        return p

    def main_loop(self, queue: Queue):                
        while self.running:
            target = queue.get()
            self.ser.write(target.serialize())



class FAKE_DEVICE(DEVICE):
    # Builds a fake device instead of a real device to mimic and verify commands

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)