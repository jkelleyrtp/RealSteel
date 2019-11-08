# This module is essentially the guts of the robot primary logic
from multiprocessing import Pool, Process, Queue
from enum import Enum

from realsteel.device import ROBOT_DEVICE, FAKE_DEVICE
from realsteel.visualizer import DEMO_VIS, ROBOT_VIS, FAKE_VIS
from realsteel.joint_input import CAMERA, KINECT, HYBRID
from realsteel.kinematic import KSOLVER
from realsteel.pathplanner import PATHPLANNER

vis_mode = Enum('demo','dev','disabled')

class ROBOT:
    """
    This code processes the launch args and sets up all the moving parts to get the REAL STEEL experience up and running.
    Nothing in this main loop should blocking, but rather pushing data around between threads. Everything should be async.

    """
    def __init__(self, hardware_enabled = False, visualization_mode = vis_mode.disabled ):
        # [1] Build the virtual robot from joints
        # [2] Set up the camera/kinect inputs to dump raw joint angles
        # [3] Set up the kinematic solver that takes raw joint angles and turns into robot angles
        # [4] Set up the path planner that maps joint angles frames
        # [5] Set up the physical robot interface
        # [6] Set up the visualizer

        # Process the user flags to process things like dev mode
        self.hardware_enabled: bool = hardware_enabled
        self.visualization_mode: vis_mode = visualization_mode

        # [1] Build the robot from a URDF file
        # TODO, allow specifying a custon URDF
        self.raw_positions: dict = None
        self.joint_positions: dict = None
        self.intialize_robot_from_urdf(file = "")

        # [2] Set up the camera/kinect input device
        self.joint_input = HYBRID()

        # [3] Set up the kinematic solver 
        self.solver = KSOLVER()

        # [4] Set up the path planner
        self.planner = PATHPLANNER()

        # [5] Set up the hardware device
        if self.hardware_enabled:
            self.device = ROBOT_DEVICE()
        else:
            self.device = FAKE_DEVICE()

        # [6] Set up the visualizer
        # Spawn a thread that sets up the visualizer
        if self.visualization_mode == vis_mode.demo:
            self.visualizer = DEMO_VIS()

        if self.visualization_mode == vis_mode.dev:
            self.visualizer = ROBOT_VIS()

        if self.visualization_mode == vis_mode.disabled:
            self.visualizer = FAKE_VIS()

    def main_loop(self):
        # Start the visualizer
        vis_proc = self.visualizer



        




