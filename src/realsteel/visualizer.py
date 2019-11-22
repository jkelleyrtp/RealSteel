import math
import sys
import pybullet as p
from realsteel.simulation import Simulation
from multiprocessing import Process, Queue


class VISUALIZER:
    def __init__(self, *args, **kwargs):
        pass
    
    def next_frame(self, new_joints: float):
        pass

class DEMO_VIS(VISUALIZER):
    """
    Visualizer for the final product (including game mechanics and such)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def launch(self):
        """
        Launches the visualizer on a new thread and responds to external input
        """
        pass

class ROBOT_VIS(VISUALIZER):
    """
    Sets up a visualizer for a single robot
    """
    def __init__(self, directory="robot"):

        self.sim = Simulation(directory)

        self.controls = {}
        for name in self.sim.getJoints():
            self.controls[name] = p.addUserDebugParameter(name, 0, 4 * math.pi, 0)

    def next_frame(self, angles: [float, float]):
        """Visuzlies next frame with shoulder and proximal angles"""
        targets = {}
        for name in self.controls.keys():
            targets[name] = p.readUserDebugParameter(self.controls[name]) % (2 * math.pi) - math.pi
        
        targets["shoulder_left"] = angles[0] 
        targets["proximal_left"] = angles[1] 

        self.sim.setJoints(targets)



class FAKE_VIS(VISUALIZER):
    """
    Sets up a fake visualizer that doesn't do much
    """    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def launch(self):
        """
        Launches the visualizer on a new thread and responds to external input
        """

        print("Hello fake visualizer!")
        pass

