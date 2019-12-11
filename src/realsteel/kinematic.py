import numpy as np
import math
import matplotlib.pyplot as plt
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
from ikpy import plot_utils

# Solve the kinematic 

class KSOLVER:
    def __init__(self, *args, **kwargs):
        self.chain = Chain(name='left_arm', links=[
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
            )
        ])

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


    def solve(self, wrist_postion):
        """Performs inverse kinematics and returns joint angles in rads
        
        For now uses one target vector at the wrist position for inverse kinematics.
        For the future, should use additional target vectors and match the elbow

        """
        # Setup target vector with target position at wrist
        target_vector = np.array([wrist_postion[0], wrist_postion[1], wrist_postion[2]])
        target_frame = np.eye(4) 
        target_frame[:3, 3] = target_vector

        joint_angles = self.chain.inverse_kinematics(target_frame)[1:3]
        print('Joint angles:', joint_angles)
        print('Computed position vector:', self.chain.forward_kinematics(self.chain.inverse_kinematics(target_frame))[:3, 3], \
            'Original position vector:', target_frame[:3, 3])

        return joint_angles


class ArmJoints():
    def __init__(self, shoulder, proximal, distal):
        self.shoulder = shoulder
        self.proximal = proximal
        self.distal = distal

    def serialize(self):
        return bytes('#{},{}!'.format(self.shoulder, self.proximal), encoding="ascii")
