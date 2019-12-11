import numpy as np
import math
import matplotlib.pyplot as plt
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
from ikpy import plot_utils
from mpl_toolkits.mplot3d import axes3d, Axes3D

# Solve the kinematic 

class KSOLVER:
    def __init__(self, *args, **kwargs):
        self.left_chain = Chain(name='left_arm', links=[
            OriginLink(),
            URDFLink(
                name="shoulder_left",
                translation_vector=[0, 0, 0],
                orientation=[-0.752186, -0.309384, -0.752186],
                rotation=[0.707107, 0, 0.707107],
            ),
            URDFLink(
                name="proximal_left",
                translation_vector=[-0.0141421, 0, 0.0424264],
                orientation=[-7.77156e-16, 7.77156e-16, 5.55112e-17],
                rotation=[-0.707107, 0, 0.707107],
            ),
            URDFLink(
                name="distal_left",
                translation_vector=[0.193394, -0.0097, 0.166524],
                orientation=[1.66533e-16, -7.21645e-16, 3.88578e-16],
                rotation=[0, -1, 0],
            ),
            URDFLink(
                name="left_tip",
                translation_vector=[-0.0431288, 0.0075, -0.133191],
                orientation=[0, -3.33067e-16, -1.11022e-16],
                rotation=[0, 1, 0],                
            )
        ])

        self.right_chain = Chain(name='right_arm', links=[
            OriginLink(),
            URDFLink(
                name="shoulder_right",
                translation_vector=[0, 0, 0],
                orientation=[-0.706606, 0.270333, 0.706606],
                rotation=[0.707107, 0, -0.707107],
            ),
            URDFLink(
                name="proximal_right",
                translation_vector=[0.0141421, -4.16334e-17, 0.0424264],
                orientation=[-0.705905, -0.269757, -0.705905],
                rotation=[0.707107, 0, 0.707107],
            ),
            URDFLink(
                name="distal_right",
                translation_vector=[-0.193394, -0.0097, 0.166524],
                orientation=[2.01609e-16, 0.811584, -3.32655e-15],
                rotation=[0, -1, 0],
            )
        ])

        plt.ion()
        # plt.show()
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


    def solve(self, wrist_postion, DEBUG=False):
        """Performs inverse kinematics and returns joint angles in rads"""
        # Setup target vector with target position at wrist
        target_vector = np.array([wrist_postion[0], wrist_postion[1], wrist_postion[2]])
        target_frame = np.eye(4) 
        target_frame[:3, 3] = target_vector

        joint_angles = self.left_chain.inverse_kinematics(target_frame)[1:4]
        # joint_angles = self.left_chain.inverse_kinematics(target_frame)[1:3]

        if DEBUG:
            # print('Joint angles:', joint_angles)
            print('Computed position vector:', self.left_chain.forward_kinematics(self.left_chain.inverse_kinematics(target_frame))[:3, 3], \
                'Original position vector:', target_frame[:3, 3])
            
            self.plot(self.left_chain.inverse_kinematics(target_frame), self.ax, target=target_vector, show=True)

        return joint_angles

    def plot(self, joints, ax, target=None, show=False):
        """Plots the Chain using Matplotlib
        Parameters
        ----------
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

        plot_utils.plot_chain(self.left_chain, joints, ax)
        plot_utils.plot_basis(ax, self.left_chain._length)

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
