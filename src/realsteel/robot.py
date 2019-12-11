# This module is essentially the guts of the robot primary logic
from multiprocessing import Pool, Process, Queue
import time, math
from enum import Enum
import numpy as np
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

        # [7] Set up robot kinematics chain
        self.left_chain = Chain(name='left_arm', links=[
            OriginLink(),
            URDFLink(
                name="shoulder_left",
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


    def start(self):
        self.main_loop()

    def main_loop(self):
        # # Set up a shared queue to put human angles into
        # input_queue = Queue()

        # # Get the process for the input method and start it
        # input_proc = self.joint_input.launch(input_queue)
        # input_proc.start()

        # # Set up the device queue to push data into
        # device_queue = Queue()
        # device_proq = self.device.launch(device_queue)
        # device_proq.start()

        # # Set the initial
        # joints = {}
        # joint_angles = [1, 1]

        # while True:
        #     # Check if there's a new human joint inputs ready
        #     # if not input_queue.empty():
        #     joints = input_queue.get()
        #     if joints['NITE_JOINT_LEFT_HAND']:
        #         left_hand = self.solver.translate_coordinates_2d(joints['NITE_JOINT_LEFT_HAND'], joints['NITE_JOINT_LEFT_SHOULDER'])
        #         left_hand = np.append(left_hand, joints['NITE_JOINT_LEFT_HAND'][2])
        #         joint_angles = self.solver.solve(left_hand)

        #         joint = ArmJoints(joint_angles[0], joint_angles[1], 0.0)

        #         device_queue.push(joint)

        # Set up a shared queue to put human angles into
        input_queue = Queue(maxsize=2)

        # Get the process for the input method and start it
        input_proc = self.joint_input.launch(input_queue)
        input_proc.start()

        # Set the initial
        joints = {}
        left_prev = np.asarray([])
        left_angles = np.asarray([0, 0, 0, 0, 0])
        right_prev = np.asarray([])
        right_angles = np.asarray([0, 0, 0, 0, 0])
        update = True

        while True:
            # Check if there's a new human joint inputs ready
            joints = input_queue.get()

            # Left Hand Kinematics
            if joints['NITE_JOINT_RIGHT_HAND']:
                # Shift pose coordinate in reference to desinated base of kinematics chain
                left_hand = self.solver.translate_coordinates(joints['NITE_JOINT_RIGHT_HAND'],
                                                 joints['NITE_JOINT_RIGHT_SHOULDER'])
                       
                # Invert the z value                                                     
                left_hand[2] = -left_hand[2]        

                # Convert from kinect's coordinate system orientaion to ikpy's orientation                                
                left_hand = self.solver.rotate_x(left_hand, math.pi/2)

                left_prev = left_angles
                left_angles = self.solver.solve(self.left_chain, left_hand, left_prev, DEBUG=False)

            # Right Hand Kinematics
            if joints['NITE_JOINT_LEFT_HAND']:
                # Shift pose coordinate in reference to desinated base of kinematics chain
                right_hand = self.solver.translate_coordinates(joints['NITE_JOINT_LEFT_HAND'],
                                                 joints['NITE_JOINT_LEFT_SHOULDER'])
                       
                # Invert the z value                                                     
                right_hand[2] = -right_hand[2]        

                # Convert from kinect's coordinate system orientaion to ikpy's orientation                                
                right_hand = self.solver.rotate_x(right_hand, math.pi/2)
                
                right_prev = right_angles
                right_angles = self.solver.solve(self.right_chain, right_hand, right_prev)


                # joint = ArmJoints(joint_angles[1], joint_angles[2], 0.0)

            # Pump out the angles to the visualizer
            self.visualizer.next_frame(left_angles[1:4], right_angles[1:4])
