import ikpy
import numpy as np
from ikpy import plot_utils

# Solve the kinematic 



class KSOLVER:
    def __init__(self, *args, **kwargs):
        pass

    def solve(self, human_anlges):
        pass




class ArmJoints():
    def __init__(self, shoulder, proximal, distal):
        self.shoulder = shoulder
        self.proximal = proximal
        self.distal = distal

    def serialize(self):
        return bytes('#{},{}!'.format(self.shoulder, self.proximal), encoding="ascii")
