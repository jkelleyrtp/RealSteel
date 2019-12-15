+++
title = "Arm Design"
weight = 40
+++

The Real Steel robot arms were some of the most fun pieces to design of the whole system. We wanted to keep the mass of the arm as close to the axis of rotation as possible - the more balanced the arms were, the faster the motors could turn them. 

## Top-Level design

To simplify the design of the complicated sensor and motor interfaces, we created a single top-level sketch of the entire robot system and derived sketches for each of the subsystems. This approach to design is a common parametric technique that allows upstream design changes without breaking everything downstream. We were able to iterate on the width of the robot's shoulders and shoulder angles while the final pieces remained relatively the same. The benefits of this approach came to fruition when we modified the arm dimensions and mass in the final sprint by changing just a few numbers and reprinting all the pieces. 



We were particularly careful to keep the mass and size of the arm to a minimum. We gave special consideration to the placement of the servo and kept the center of mass as close to the shaft axis of rotation as possible. This gave the arm a fairly low mass moment of angular inertia. We used a simple linkage to transfer the servo's torque to the elbow which kept the weight down and allowed us to get a simple torque multiplier in with little effort. By maintaining a low profile on the arm components, the robot had a greater range of motion and could move fast enough for real-time movements. 

<center> {{ resize_image(path="documentation/hardware/Arm/Untitled.png", width=0, height=500, op="fit_height") }} </center>

<div class="row">
  <div class="column">
    <center> {{ resize_image(path="documentation/hardware/Arm/Untitled 3.png", width=0, height=300, op="fit_height") }} </center>
  </div>
  <div class="column">
    <center> {{ resize_image(path="documentation/hardware/Arm/Untitled 1.png", width=0, height=300, op="fit_height") }} </center>
  </div>
</div>

We were also careful to design with failure in mind. At the major interfaces, we chose to separate the single part into two parts fastened together. Specifically for the arm, the hub that connected it to the driving motor was removable from the primary arm component. We happened to print the dimensions improperly a few times before getting the design dialed in, and the separation between hub and arm was vital to keep the iteration time as fas as possible.

<center> {{ resize_image(path="documentation/hardware/Arm/Untitled 2.png", width=0, height=500, op="fit_height") }} </center>

<style>
    .row {
    display: flex;
    }

    .column {
    flex: 50%;
    }
</style>