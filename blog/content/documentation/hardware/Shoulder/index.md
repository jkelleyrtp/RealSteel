+++
title = "Shoulder Design"
weight = 35
+++

The shoulders of the Real Steel robots were fun to design and pulled in some interesting 3D print techniques. We created an adapter system that used the profile of the motor shafts to fasten the hubs onto the primary body parts. This let us gracefully handle failures and more easily replace broken components. We also designed and 3D-printed our own gears which were used in conjunction with the custom encoder boards to get position feedback of the joints back to the STM32 controller. 

<div class="row">
  <div class="column">
    <center> {{ resize_image(path="documentation/hardware/Shoulder/Untitled.png", width=0, height=500, op="fit_height") }} </center>
  </div>
  <div class="column">
    <center> {{ resize_image(path="documentation/hardware/Shoulder/Untitled 2.png", width=0, height=500, op="fit_height") }} </center>
  </div>
</div>

<div>

</div>

<style>
    .row {
    display: flex;
    }

    .column {
    flex: 50%;
    }
</style>

One of the most interesting components of the shoulder system was the design of a custom parametric slew bearing which could adapt to any size we needed. We stuck with one size and honed in the sizes to be amenable for 3D printing. The slew bearings were able to take high axial and radial loads and were fast to manufacture. 

<center> {{ resize_image(path="documentation/hardware/Shoulder/Untitled 1.png", width=0, height=300, op="fit_height") }} </center>

