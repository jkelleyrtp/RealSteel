+++

title = "Overview"

weight = 10

+++

This documentation provides a set of information and resources on how to design, build, and program and shadow-boxing robot for less than $250. This was an exceptionally ambitious Principles of Engineering project and required advanced skills in CAD, CAM, math, firmware, software, and systems integration. Each component of the system -  whether it be the serial output format of the robot joints or the location of the elbow linkage - was dependent on the other components. This led to an incredibly carefully designed collection of components that pushed the limits of Olin's 3D printers, the STM32 microcontroller, and the compute power of the school laptops. 

<center>
    {{ resize_image(path="documentation/overview/Overview/reaganbot.png", width=0, height=500, op="fit_height") }}
</center>

## Final Feature Set

The final featureset of the Real Steel shadow-boxing robot is quite amazing:

- 8 Degrees of freedom - two arms and a hip system
- The ability to bob, weave, throw punches, and dab, all in real time
- 8 real-time PID controllers maintaining closed-loop control of the robot joint positions
- Real time pose estimation using a Time-of-Flight depth sensor
- Real-time kinematic solving of a 3 DoF robotic arm from a human's 7 DoF
- A portable Python-based multithreaded framework for data collection, processing, visualization, and serial output
- Pre-programmed positions for control without the kinect

## Challenges and Constraints

We ran into several challenges while designing and building the Real Steel robot. These included:

- Limited microcontroller inputs 12 quadrature encoders (2 robots worth, ran out after 1 robot)
- Limited outputs to control all the motor outputs
- Limited electrical power to power all motors simultaneously
- Limited compute power to process the kinect data and convert it into a serial packet with joint information
- Limited mechanical strength on 3D printed parts to handle the forces involved in moving the robot around

The following sections address these challenges and provide further insights on how the final feature set came together.