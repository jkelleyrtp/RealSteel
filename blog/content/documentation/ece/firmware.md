+++
title = "Firmware Overview"
weight = 10
+++

The robot firmware had one job: take a setpoint over serial and maintain closed-loop control over the robot subsystems. We used PWM to communicate with each of the motor controllers and an external power supply to power everything, so the firmware simply needed to output a signal for each motor. 

The setpoint came in over serial and was decoded by a custom bson interpreter written in C++. We used the STM32 chip on the Nucleo F446ZE development board as the microcontroller, and reused PID control from the last PoE lab for closed-loop control. As our port and compute capacity was limited, the predictive control was all implemented on the host software.