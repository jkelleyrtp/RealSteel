# This module is essentially the guts of the robot primary logic
from multiprocessing import Pool, Process, Queue
import time
from enum import Enum

from realsteel.device import ROBOT_DEVICE, FAKE_DEVICE
from realsteel.visualizer import DEMO_VIS, ROBOT_VIS, FAKE_VIS
from realsteel.joint_input import CAMERA, KINECT, HYBRID
from realsteel.kinematic import KSOLVER
from realsteel.pathplanner import PATHPLANNER

# vis_mode = Enum('demo','dev','disabled')

class ROBOT:
    """
    This code processes the launch args and sets up all the moving parts to get the REAL STEEL experience up and running.
    Nothing in this main loop should blocking, but rather pushing data around between threads. Everything should be async.

    """
    def __init__(self, hardware_enabled = False, visualization_mode="disabled"):
        # [1] Build the virtual robot from joints
        # [2] Set up the camera/kinect inputs to dump raw joint angles
        # [3] Set up the kinematic solver that takes raw joint angles and turns into robot angles
        # [4] Set up the path planner that maps joint angles frames
        # [5] Set up the physical robot interface
        # [6] Set up the visualizer

        # Process the user flags to process things like dev mode
        self.hardware_enabled: bool = hardware_enabled
        self.visualization_mode = visualization_mode

        # [1] Build the robot from a URDF file
        # TODO, allow specifying a custon URDF
        self.human_positions: dict = None
        self.robot_positions: dict = None
        # self.intialize_robot_from_urdf(file = "")

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
        if self.visualization_mode == "dev":
            self.visualizer = ROBOT_VIS(directory='robot/')

        elif self.visualization_mode == "demo":
            self.visualizer = DEMO_VIS()

        else:
            self.visualizer = FAKE_VIS()


    def start(self):
        self.main_loop()

    def main_loop(self):
        # Set up a shared queue to put human angles into
        input_queue = Queue()

        input_queue.push()

        a = input_queue.get_nowait()

        # Get the process for the input method and start it
        input_proc = self.joint_input.launch(input_queue)
        input_proc.start()

        # Set the initial
        joints = {}
        joint_angles = [1, 1]

        while True:
            # Check if there's a new human joint inputs ready
            if not input_queue.empty():
                joints = input_queue.get()
                if joints['Lwri']:
                    joint_angles = self.solver.solve(joints['Lwri']['pc'])

            # Pump out the angles to the visualizer
            self.visualizer.next_frame(pos)
