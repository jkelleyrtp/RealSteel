+++
title = "Torso Design"
weight = 30
+++

The torso of the Real Steel robots was one of the more complicated parts of the robot to design. Not only did it have to integrate with the robot base, but it had to support both arms, the head, and the accompanying sensors to maintain accurate position control over the shoulder joints. The final design of the robot body came together in 5 separate pieces: the torso, the shoulder supports, the stand balance plate, and the head. 

The adapter plate was designed to simply bolt into the bottom of the primary torso part. We iterated several times on the adapter plate to allow for the "bob" and "weave" ranges of motion, and settled on the adapter plate design to allow for modifications to be made without having to reprint the torso. in fact, the torso itself is 3 separate pieces fastened together with bolts, plastic inserts, and CA glue.

<center>
    {{ resize_image(path="documentation/hardware/Torso/Untitled.png", width=0, height=500, op="fit_height") }}
</center>

We spent a lot of time iterating on the placement of motors and sensors on the torso. Shown below is the strange placement of the shoulder motor embedded deep into the torso. The wires were mostly inaccessible and had to be wired and soldered before installation. For proper assembly, the motor had to be dropped into the torso, the shoulder mound had to be fastened, and then we could finally mount the motor to the rest of the shoulder. However, the final design was very strong and with clever 3D printing, we achieved a robust torso design operating at near maximum PLA strength (more in some areas!) that gracefully took a few falls off the assembly table.

<center>
    {{ resize_image(path="documentation/hardware/Torso/Untitled 1.png", width=0, height=500, op="fit_height") }}
</center>