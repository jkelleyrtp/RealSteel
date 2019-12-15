+++
title = "Human Tracking"
weight = 20
+++

## Human Tracking

We use the Kinect v1 camera to perform human skeleton tracking using its IR camera. We interface with the Kinect using the OpenNI2 library for core Kinect features and NiTE2 for skeleton tracking purposes. To support the Kinect v1 camera with these two libraries, the OpenNI2-FreenectDriver bridge must also be installed. These libraries allow us to develop in non-windows platforms using opensource software.

### Dependency Installation

There are difficulties in getting these dependencies installed as the OpenNI and NiTE project was discontinued when Apple bought PrimeSense. Instead, these packages are now hosted and can be downloaded using the following guide:

[https://github.com/roboticslab-uc3m/installation-guides/blob/master/install-openni-nite.md](https://github.com/roboticslab-uc3m/installation-guides/blob/master/install-openni-nite.md)

### Skeleton Tracking

Using NiTE2 we access skeleton tracking information from the Kinect. At each frame we obtain the position of all 15 joints as (x, y, z) coordinates. 



<center>

![Untitled.png](Untitled.png)
</center>

### Coordinate System

The Kinect and OpenNI has two coordinate systems used. These two systems are referred to as Depth and World representation. The differences can be described like so:

1. Depth coordinates
    - the native data representation
    - the origin is the top-left corner of the field of view
    - x and y coordinates are reference to the image frame pixels
    - the depth value represents the distance between the camera plane and whatever object is in the given pixel
2. World coordinates
    - superimpose a more familiar 3D Cartesian coordinate system on the world
    - the origin is at the Kinect camera lens
    - every point is specified by 3 points (x, y , z) in millimeters

<center>

![Untitled%201.png](Untitled%201.png)
</center>

We obtain the joint information and can convert between both systems depending on our needs.