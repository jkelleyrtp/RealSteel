+++
title = "Sensors"
weight = 20
+++

We designed a handful of custom sensor to make the feedback collection easier. One important sensor we designed was a simple quadrature encoder board with a dial knob. This allowed us to integrate the gears onto the encoders with ease, and each board was exceptionally cheap at only $2 per.

<center> {{ resize_image(path="documentation/ece/Sensors/Untitled.png", width=0, height=500, op="fit_height") }} </center>

As 8 quadrature encoders is simply too much information for the STM32 to handle at once, we also developed a simple quadrature interpreter board after we had designed the quadrature encoders. This counted the number of steps the quadrature encoder had performed and stored them so the firmware wouldn't have to keep track manually. These boards were powered by a simple STM8 and output their data over I2C. This gave us an incredible performance boost and allowed us to keep closed-loop control of the robot arms and hip system without the controller breaking a sweat.

<center> {{ resize_image(path="documentation/ece/Sensors/Untitled 1.png", width=0, height=500, op="fit_height") }} </center>
