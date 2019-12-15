+++
title = "Controls and Feedback"
weight = 30
+++

## Motor control:

A simple PID controller was used for motor control. However, we were able to run it at 1kHz due to the floating point accelerator on the STM32F446, allowing for extremely high gain feedback.

## Motor controller boards:

We decided to be thrifty and copied 1:1 Adafruit's DRV8871 motor controller boards, saving us a large amount of money compared to what we'd have to spend on 12 genuine ones.

<center> {{ resize_image(path="documentation/ece/controls/Untitled.png", width=0, height=500, op="fit_height") }} </center>
