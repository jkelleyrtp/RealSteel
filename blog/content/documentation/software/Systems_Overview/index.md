+++
title = "Software Overview"
weight = 10
+++

The software powering Real Steel is fairly complex, but we chose a handful of architectural patterns and libraries to simplify the development process. Our language of choice was Python and we relied heavily on `OpenNI` for kinect-related libraries, Python's `Multiprocessing` library for concurrency, `ikpy` for forward kinematic solving, `pybullet` for simulation of the robot, and `PySerial` to get the joint angle to the robot.

<center>
    {{ resize_image(path="documentation/software/Systems_Overview/Untitled.png", width=0, height=500, op="fit_height") }}
</center>


All of these components were given their own `class` in the Python code, and inherited certain functionality so that we could easily disable and enable different parts of the code with a few flags. For instance, the python code that loads in all the modules is fairly simple, despite the entire codebase being several thousand lines. We chose the pipeline architecture and separated each of the components into their own submodules to be more easily unit-testable. The entire system can run with "fake" components which satisfy the software requirements and even create fake data so we can do integration tests with entire chunks of the pipeline missing. This is a solid, industry-practiced software engineering tactic that allowed us to iterate faster and modularize our code.


```python
from realsteel.device import ROBOT_DEVICE, FAKE_DEVICE
from realsteel.visualizer import DEMO_VIS, ROBOT_VIS, FAKE_VIS
from realsteel.joint_input import CAMERA, KINECT, HYBRID
from realsteel.kinematic import KSOLVER
from realsteel.pathplanner import PATHPLANNER
from realsteel.kinematic import ArmJoints


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
```