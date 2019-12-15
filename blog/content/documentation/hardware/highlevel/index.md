+++
title = "High Level Design"
weight = 10
+++

We faced a significant challenge in integrating the mechanical and electrical aspects of the project; each additional component added more complexity and points of failure. To mitigate the potential non-obvious potholes, we decided to start designing the system from a high-level first before diving into the details. 

Our mechanical system had a handful of requirements:

- The ability to "throw a punch"
- The ability to "bob and weave"
- The ability to "block a punch"

This ultimately manifested itself into a robot with:

- Two arms
- 3 DoF per arm (shoulder, proximal, and distal)
- 2 DoF hip system

Using OnShape as our CAD software of choice, we sketched out the high-level geometry, making sure to maintain realistic dimensions and leave room for important components like servos, motors, and sensors. The system sketch was used in "derive" mode to generate the rest of the subsystems.


<center> {{ resize_image(path="documentation/hardware/highlevel/Untitled.png", width=0, height=500, op="fit_height") }} </center>
