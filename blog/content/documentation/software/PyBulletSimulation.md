+++
title = "PyBullet Simulation"
weight = 40
+++


## PyBullet Simulation

Before we send the joint coordinates over serial to the actual robot, we want to ensure that our methodology and solutions are correct. Therefore, we use PyBullet, a physics engine, to simulate our robot movements.

<center>
    {{ resize_image(path="documentation/software/Inverse_Kinematics/Untitled 3.png", width=0, height=200, op="fit_height") }}
</center>


Loading in our URDF file for the robot, we can pump in the joint angles and see how a virtual replica of our robot would behave under proper physics.

[https://youtu.be/1XufNJylf4Q](https://youtu.be/1XufNJylf4Q)
