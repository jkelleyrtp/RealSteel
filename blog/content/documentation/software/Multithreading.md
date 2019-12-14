+++

title = "Multithreaded Framework"

weight = 50

+++

## Multithreaded Framework

In order to perform the skeleton tracking, joint solving, visualizations, and communication all together  simultaneously, we set up a multithreaded framework centered around python's multiprocessing Queues. In our framework, we use two queues: an input queue and a device/output queue. 

The input queue gets Kinect joint information pushed into it at every frame. The other systems, inverse kinematics and visualizations, pop joint information off of this queue as long as it's not empty for processing.

The device queue gets robot joint angles pushed into it at every iteration of the main robot loop and communicates these angles over serial whenever they are available.