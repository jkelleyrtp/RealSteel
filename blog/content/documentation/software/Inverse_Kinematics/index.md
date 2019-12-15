+++
title = "Inverse Kinematics"
weight = 30
+++

## Inverse Kinematics

Inverse Kinematics is needed to map human movement into robot movement. This is because, calculating joint angles using human extracted joints doesn't translate to robot joint angles. We have different joints than the robot and at different positions and lengths. Instead, using an inverse kinematics solver an articulated body can be programmed to reach a certain target position with its end effector.

<center>

![https://media1.giphy.com/media/HLyej9afegzcc/giphy.gif](https://media1.giphy.com/media/HLyej9afegzcc/giphy.gif)
</center>

In RealSteel's robots, we have the following revolute joints in an arm:

1. Shoulder
2. Proximal
3. Distal

<center>
    {{ resize_image(path="documentation/software/Inverse_Kinematics/Untitled.png", width=0, height=500, op="fit_height") }}
</center>


### How Does It Work?

Given a target position, how can we position the articulated body and all it's joints such that the end effector reaches the target? An inverse kinematics solver answers this question with two categories of solutions:

1. Analytic solutions
2. Approximating solutions

We use ikpy, an inverse kinematics library, that can quickly approximate the solution with an iterative optimizer with regularization for smoothing.

<center>
    {{ resize_image(path="documentation/software/Inverse_Kinematics/Untitled 1.png", width=0, height=500, op="fit_height") }}
</center>

ikpy also can import the kinematic chain to solve as long as the robot is defined in URDF format. Luckily for us, we designed our own robot in OnShape and using onshape-to-robot we can convert our OnShape assembly to URDF robot definition.

### ikpy Coordinate System

ikpy defines its kinematic chain to start at the origin in a coordinate system that is rotated 90° about the x-axis compared to the Kinect coordinate system. We also run into an issue as the Kinect tracks joint positions with respect to a fixed origin at the center of it's camera lens and not at the base of the kinematic chain - the origin that ikpy expects. Therefore, any target position that we want to solve for with ikpy will be misinterpreted.

The solution is to transform the target joint's (the hand joint) position from the Kinect frame to a frame that has it's origin fixed at the shoulder joint of the arm that is being solved for. The z or depth value is then inverted to place depth in front of the person, and the point is rotated 90° about the x-axis. This way now the kinematic chain and target joint position are in the same frame of reference, and ikpy can solve correctly.

<center>
    {{ resize_image(path="documentation/software/Inverse_Kinematics/Untitled 2.png", width=0, height=400, op="fit_height") }}
</center>

### The Process

With all the tools in place, we can now proceed with solving for our robot joint angles in real-time in the following steps (note: this is done independently for both arms each)

1. Obtain robot model in URDF format
2. Import model into ikpy and define a base_element to start the kinematic chain at the shoulder joint of an arm
3. Obtain target position from the Kinect → the world coordinates for skeletal joint at the hand for the corresponding arm
4. Perform the necessary transforms to get the target into ikpy coordinate system
5. Solve for joint angles

[https://youtu.be/kSUGiyJ5UbY](https://youtu.be/kSUGiyJ5UbY)
