import numpy as np
import math
import matplotlib.pyplot as plt
from ikpy import plot_utils
from ikpy import inverse_kinematics
from mpl_toolkits.mplot3d import axes3d, Axes3D

# Solve the kinematic 
class KSOLVER:
    def __init__(self, *args, **kwargs):
        # Setup plotting
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

    def translate_coordinates(self, position_global, new_origin):
        """Translates a point in the global coordinate system to one relative to a new origin"""
        position_global = np.array([position_global[0], position_global[1], position_global[2], 1])
        t_matrix = np.array([[1, 0 , 0, -new_origin[0]], 
                            [0, 1 , 0, -new_origin[1]], 
                            [0, 0 ,1, -new_origin[2]],
                            [0, 0, 0, 1]])
        return (t_matrix @ position_global)[0:3]

    def rotate_x(self, p, angle):
        """Rotates a 3D point around the x axis"""
        t_matrix = np.array([[1, 0 , 0], 
                            [0, math.cos(angle) , -math.sin(angle)], 
                            [0, math.sin(angle) , math.cos(angle)]])
        return t_matrix @ p


    def solve(self, chain, target, prev_angles, DEBUG=False):
        """Performs inverse kinematics and returns joint angles in rads"""
        # Setup target vector with target position at wrist
        target_vector = np.array([target[0], target[1], target[2]])
        target_frame = np.eye(4) 
        target_frame[:3, 3] = target_vector

        joint_angles = inverse_kinematics.inverse_kinematic_optimization(chain, target_frame, prev_angles, .001)
        
        if DEBUG:
            print('Computed position vector:', chain.forward_kinematics(joint_angles)[:3, 3], \
                'Original position vector:', target_frame[:3, 3])
            
            self.plot(chain, joint_angles, self.ax, target=target_vector, show=True)
            
        return joint_angles

    def plot(self, chain, joints, ax, target=None, show=False):
        """Plots the Chain using Matplotlib
        Parameters
        ----------
        chain: ikpy.chain.Chain
            The chain used for the Inverse kinematics.
        joints: list
            The list of the positions of each joint
        ax: matplotlib.axes.Axes
            A matplotlib axes
        target: numpy.array
            An optional target
        show: bool
            Display the axe. Defaults to False
        """
        self.ax.clear()

        plot_utils.plot_chain(chain, joints, ax)
        plot_utils.plot_basis(ax, chain._length)

        ax.set_xlim3d([-.3, .3])
        ax.set_ylim3d([-.3, .3])
        ax.set_zlim3d([-.3, .3])

        # Plot the goal position
        if target is not None:
            plot_utils.plot_target(target, ax)
        if show:
            plt.draw()
            self.fig.canvas.flush_events()

class ArmJoints():
    def __init__(self, shoulder, proximal, distal):
        self.shoulder = shoulder
        self.proximal = proximal
        self.distal = distal

    def serialize(self):
        return bytes('#{},{}!'.format(self.shoulder, self.proximal), encoding="ascii")
