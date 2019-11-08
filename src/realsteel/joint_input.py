# This module takes in raw input devices and produces the raw angles
from multiprocessing import Process, Queue
import time

class JOINT_INPUT:
    def __init__(self, *args, **kwargs):
        pass

class CAMERA(JOINT_INPUT):
    """
    Sets up the camera-only pipeline
    """
    def __init__(self, *args, **kwargs):
        pass

class KINECT(JOINT_INPUT):
    """
    Sets up the kinect-only pipeline
    """
    def __init__(self, *args, **kwargs):
        pass

class HYBRID(JOINT_INPUT):
    """
    Sets up the hybrid pipeline
    """
    def __init__(self, *args, **kwargs):
        pass

    def launch(self, queue):
        q = queue
        p = Process(target=self.main_loop, args=(q,))
        return p

    def main_loop(self, queue: Queue):
        i = 0
        while True:
            time.sleep(.00025)
            i += .01
            queue.put(i)