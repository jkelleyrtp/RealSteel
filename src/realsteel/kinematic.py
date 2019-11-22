import numpy as np
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
            translation_vector=[0.13182, -2.77556e-17, 0.303536],
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

    def solve(self, wrist_postion):
        """Performs inverse kinematics and returns joint angles in rads
        
        For now uses one target vector at the wrist position for inverse kinematics.
        For the future, should use additional target vectors and match the elbow

        """
        # TODO: Fix coordinate system transform for extra degree of freedom rotation
        # Setup target vector with target position at wrist
        target_vector = np.array([wrist_postion[0], wrist_postion[1], wrist_postion[2]])
        target_frame = np.eye(4) 
        target_frame[:3, 3] = target_vector

        joint_angles = self.chain.inverse_kinematics(target_frame)[1:3]
        print('Joint angles:', joint_angles)
        print('Computed position vector:', self.chain.forward_kinematics(self.chain.inverse_kinematics(target_frame))[:3, 3], \
            'Original position vector:', target_frame[:3, 3])

        joints = self.chain.inverse_kinematics(target_frame)[1:3]

        return np.array([0, joints[1]])


class ArmJoints():
    def __init__(self, shoulder, proximal, distal):
        self.shoulder = shoulder
        self.proximal = proximal
        self.distal = distal

    def serialize(self):
        return bytes('#{},{}!'.format(self.shoulder, self.proximal), encoding="ascii")
