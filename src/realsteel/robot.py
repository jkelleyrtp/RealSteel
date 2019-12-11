# This module is essentially the guts of the robot primary logic
from multiprocessing import Pool, Process, Queue
import time, math
from enum import Enum
import numpy as np
import atexit
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink

from realsteel.device import ROBOT_DEVICE, FAKE_DEVICE
from realsteel.visualizer import DEMO_VIS, ROBOT_VIS, FAKE_VIS
from realsteel.joint_input import CAMERA, KINECT, HYBRID
from realsteel.kinematic import KSOLVER
from realsteel.pathplanner import PATHPLANNER
from realsteel.kinematic import ArmJoints


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
        # [7] Set up robot kinematics chain

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
        self.input_queue = None

        # [3] Set up the kinematic solver 
        self.solver = KSOLVER()

        # [4] Set up the path planner
        self.planner = PATHPLANNER()

        # [5] Set up the hardware device
        if self.hardware_enabled:
            self.device = ROBOT_DEVICE()
        else:
            self.device = FAKE_DEVICE()
        self.device_queue = None

        # [6] Set up the visualizer
        if self.visualization_mode == "dev":
            self.visualizer = ROBOT_VIS(directory='robot/')
        elif self.visualization_mode == "demo":
            self.visualizer = DEMO_VIS()
        else:
            self.visualizer = FAKE_VIS()

        # [7] Set up robot kinematics chain
        self.left_chain = Chain(name='left_arm', links=[
            OriginLink(),
            URDFLink(
                name="shoulder_left",
                bounds=(1.745, 5.76),
                translation_vector=[0, 0, 0],
                orientation=[-0.752186, -0.309384, -0.752186],
                rotation=[0.707107, 0, 0.707107],
            ),
            URDFLink(
                name="proximal_left",
                bounds=(-1.571, 1.92),
                translation_vector=[-0.0141421, 0, 0.0424264],
                orientation=[-7.77156e-16, 7.77156e-16, 5.55112e-17],
                rotation=[-0.707107, 0, 0.707107],
            ),
            URDFLink(
                name="distal_left",
                bounds=(0, 2.0944),
                translation_vector=[0.193394, -0.0097, 0.166524],
                orientation=[1.66533e-16, -7.21645e-16, 3.88578e-16],
                rotation=[0, -1, 0],
            ),
            URDFLink(
                name="left_tip",
                translation_vector=[-0.0431288, 0.0075, -0.133191],
                orientation=[0, -3.33067e-16, -1.11022e-16],
                rotation=[0, 1, 0],                
            )
        ])

        self.right_chain = Chain(name='right_arm', links=[
            OriginLink(),
            URDFLink(
                name="shoulder_right",
                bounds=(1.745, 5.76),
                translation_vector=[0, 0, 0],
                orientation=[-0.706606, 0.270333, 0.706606],
                rotation=[0.707107, 0, -0.707107],
            ),
            URDFLink(
                name="proximal_right",
                bounds=(-1.92, 1.571),
                translation_vector=[0.0141421, -4.16334e-17, 0.0424264],
                orientation=[-0.705905, -0.269757, -0.705905],
                rotation=[0.707107, 0, 0.707107],
            ),
            URDFLink(
                name="distal_right",
                bounds=(-2.094, 0),
                translation_vector=[-0.115612, -0.0097, 0.0887419],
                orientation=[4.03219e-17, 0.811584, -3.72977e-15],
                rotation=[0, -1, 0],
            ),
            URDFLink(
                name="right_tip",
                translation_vector=[0.0431288, 0.0075, -0.133191],
                orientation=[-2.77556e-17, 5.55112e-17, -7.84095e-15],
                rotation=[0, -1, 0],                
            )
        ])

        self.left_chain.first_active_joint = 0
        self.right_chain.first_active_joint = 0

        atexit.register(self.cleanup)


    def start(self):
        self.main_loop()

    def cleanup(self):
        if self.input_queue is not None:
            while not self.input_queue.empty():
                input_queue.get()

        if self.device_queue is not None:
            while not self.device_queue.empty():
                device_queue.get()

    def reset(self):
        """Resets robot to zero position"""
        r_shoulder = [-.33, .2, 1.52]
        r_hand = [-.37, .22, 1.36]
        l_shoulder = [.01, .23, 1.46]
        l_hand = [-.02, .23, 1.27]

        left_hand = self.get_target(l_hand, l_shoulder)
        right_hand = self.get_target(r_hand, r_shoulder)

        left_angles = self.solver.solve(self.left_chain, left_hand)
        right_angles = self.solver.solve(self.right_chain, right_hand)

        return left_angles[1:4], right_angles[1:4]
    
    def get_target(self, hand, shoulder):
        """Performs a series of coordinate transforms to get target in the right frame"""
        # Shift pose coordinate in reference to desinated base of kinematics chain
        target = self.solver.translate_coordinates(hand, shoulder)
            
        # Invert the z value                                                     
        target[2] = -target[2]        

        # Convert from kinect's coordinate system orientaion to ikpy's orientation                                
        target = self.solver.rotate_x(target, math.pi/2)

        return target

    def main_loop(self):
        # Set up a shared queue to put human angles into
        self.input_queue = Queue(maxsize=3)

        # Get the process for the input method and start it
        input_proc = self.joint_input.launch(self.input_queue)
        input_proc.start()

        if self.visualization_mode == "demo":
            # Set up the device queue to push data into
            self.device_queue = Queue(maxsize=3)
            device_proq = self.device.launch(self.device_queue)
            device_proq.start()

        # Set the initial
        joints = {}
        left_prev = []
        left_angles = [0, 0, 0, 0, 0]
        right_prev = []
        right_angles = [0, 0, 0, 0, 0]

        while True:
            # Check if there's a new human joint inputs ready
            if not self.input_queue.empty():
                joints = self.input_queue.get()

                # Left Hand Kinematics
                if joints['NITE_JOINT_RIGHT_HAND']:
                    left_hand = self.get_target(joints['NITE_JOINT_RIGHT_HAND'],
                                                    joints['NITE_JOINT_RIGHT_SHOULDER'])

                    left_prev = left_angles
                    left_angles = self.solver.solve(self.left_chain, left_hand, left_prev, DEBUG=False)

                # Right Hand Kinematics
                if joints['NITE_JOINT_LEFT_HAND']:
                    right_hand = self.get_target(joints['NITE_JOINT_LEFT_HAND'],
                                                    joints['NITE_JOINT_LEFT_SHOULDER'])

                    right_prev = right_angles
                    right_angles = self.solver.solve(self.right_chain, right_hand, right_prev)

                if self.visualization_mode == "demo":
                    # Get joint data into serial protocol
                    joint = ArmJoints(left_angles[1:4], rightangles[1:4])
                    device_queue.push(joint)

            if self.visualization_mode == "dev":
                try:
                    # Pump out the angles to the visualizer
                    self.visualizer.next_frame(left_angles[1:4], right_angles[1:4])
                    # self.visualizer.next_frame([0,0,0], [0,0,0])
                    # l, r = self.reset()
                    # self.visualizer.next_frame(l, r)
                except:
                    break
