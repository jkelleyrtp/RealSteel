+++
title = "Multithreaded Framework"
weight = 50
+++

## Multithreaded Framework

In order to perform the skeleton tracking, joint solving, visualizations, and communication all together  simultaneously, we set up a multithreaded framework centered around python's multiprocessing Queues. In our framework, we use two queues: an input queue and a device/output queue. 

The input queue gets Kinect joint information pushed into it at every frame. The other systems, inverse kinematics and visualizations, pop joint information off of this queue as long as it's not empty for processing.

The device queue gets robot joint angles pushed into it at every iteration of the main robot loop and communicates these angles over serial whenever they are available.


```python
def main_loop(self):
	# Set up a shared queue to put human angles into
	input_queue = Queue()
	
	
	# Get the process for the input method and start it
	input_proc = self.joint_input.launch(input_queue)
	input_proc.start()
	
	# Set up the device queue to push data into
	device_queue = Queue()
	device_proq = self.device.launch(device_queue)
	device_proq.start()
	
	# Set the initial joint angles
	joints = {}
	joint_angles = [1, 1]
	
	while True:
		# Check if there's a new human joint inputs ready
		# if not input_queue.empty():
		joints = input_queue.get()
		if joints['Lwri']:
			joint_angles = self.solver.solve(joints['Lwri']['pc'])
	
			joint = ArmJoints(joint_angles[0], joint_angles[1], 0.0)
	
			device_queue.push(joint)
```

This architecture is the exact same architecture used in microprocessors and the technique is known as "pipelining." Just by properly designing the architecture of our code, we saw up to 60-80% performance improvement which was crucial for real time actuation.

<center>
    {{ resize_image(path="documentation/software/Multithreading/Untitled.png", width=0, height=500, op="fit_height") }}
</center>
