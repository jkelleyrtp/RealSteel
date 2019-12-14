+++

title = "Serial Output"

weight = 60

+++

 

To communicate with the Real Steel robots, we initialized a serial interface with the STM32 microcontroller (the robot's brain) to send joint positions and other information. We set up the serial interface in a separate thread as to not slow down the main thread responsible for moving data in between each of the system components. This let us maintain a 1 kHz control loop between the master computer and Real Steel robot without any performance impact on the rest of the software system.

To communicate, we used the bson minified data format - a compressed version of csv with a fixed schema based on packet length. We also developed a custom interpreter for the STM32 as there were no obvious choices that fit on an embedded system to interpret the serial data. The final format for commands between the computer and robot followed as such:

```rust

	#[derive(debug, fmt)]
	enum MessageTypes {
		setpoint(RobotSetpoint)
	}

	impl serialize for MessageTypes {
		fn serialize() -> String {
			match Self {
				MessageTypes::setpoint(setpoint) -> {
					return format!(
						"0",
						setpoint.left_shoulder,
						setpoint.left_proximal,
						setpoint.left_distal: usize,
						setpoint.right_shoulder,
						setpoint.right_proximal,
						setpoint.right_distal,
						pitch: usize,
						roll: uszie
					)
				}
			}
		}
	}

	#[derive(debug, fmt)]
	struct RobotSetpoint {
		left_shoulder: usize,
		left_proximal: usize,
		left_distal: usize,
		right_shoulder: usize,
		right_proximal: usize,
		right_distal: usize,
		pitch: usize,
		roll: uszie
	}
```

With this format, we could easily serialize and deserialize robot setpoints from the kinematic solver and convert them into a message that the robot could interpret. Messages could be of variable length, with the expected length determined by the leading digit for the packet. As shown above, the leading digit for the RobotSetpoint is 0 - so the stm32 can easily decode the robot position over a simple serial packet.