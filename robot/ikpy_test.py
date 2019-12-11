import numpy as np
import matplotlib.pyplot as plt
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
from ikpy import plot_utils

def translate_coordinates(position_global, new_origin):
  """Translates a point in the global coordinate system to one relative to a new origin"""
  position_global = np.array([position_global[0], position_global[1], position_global[2], 1])
  t_matrix = np.array([[1, 0 , 0, -new_origin[0]], 
                      [0, 1 , 0, -new_origin[1]], 
                      [0, 0 ,1, -new_origin[2]],
                      [0, 0, 0, 1]])
  return (t_matrix @ position_global)[0:3]

def rotate_x(p, angle):
  """Rotates a 3D point around the x axis"""
  t_matrix = np.array([[1, 0 , 0], 
                      [0, math.cos(angle) , -math.sin(angle)], 
                      [0, math.sin(angle) , math.cos(angle)]])
  return t_matrix @ p


def solve(chain, wrist_postion):
  """Performs inverse kinematics and returns joint angles in rads"""
  # Setup target vector with target position at wrist
  target_vector = np.array([wrist_postion[0], wrist_postion[1], wrist_postion[2]])
  target_frame = np.eye(4) 
  target_frame[:3, 3] = target_vector

  joint_angles = chain.inverse_kinematics(target_frame)[1:4]
  print('Joint angles:', joint_angles)
  print('Computed position vector:', chain.forward_kinematics(chain.inverse_kinematics(target_frame))[:3, 3], \
      'Original position vector:', target_frame[:3, 3])


  ax = plot_utils.init_3d_figure() 
  chain.plot(chain.inverse_kinematics(target_frame), ax, target=target_vector, show=True) 


  return joint_angles

left_chain = Chain(name='left_arm', links=[
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
# my_chain = Chain.from_urdf_file("robot.urdf", \
#     ["shoulder_left", "part_2_1", "proximal_left", "part_3_1", "distal_left"], \
#     base_element_type="joint") # active_links_mask=[True, True, False, False, False]

# Computed position vector: [0.0678265  0.24306558 0.3067424 ] Original position vector: [-1.195   4.1715  0.13  ]

# Computed position vector: [ 0.12592243 -0.23047451  0.20911684] Original position vector: [ 0.09679721 -0.56544003  0.05133673]

# (-0.018213945388793944, 0.2764237365722656, 1.286739990234375) shoulder
# (0.03636528015136719, 0.09349619293212891, 0.787177490234375) hand

shoulder = (-0.018213945388793944, 0.2764237365722656, 1.286739990234375)
hand = (0.03636528015136719, 0.09349619293212891, 0.787177490234375)

left_hand = translate_coordinates(hand, shoulder)

solve(left_chain, [0.21335579,  0.00382629, -0.57779678])


# target_vector = [0.09679721, -0.05133673,  -0.56544003] 
# target_frame = np.eye(4) 
# target_frame[:3, 3] = target_vector

# print('Joint angles:', left_arm_chain.inverse_kinematics(target_frame)[1:3])
# print('Computed position vector:', left_arm_chain.forward_kinematics(left_arm_chain.inverse_kinematics(target_frame))[:3, 3], \
#     'Original position vector:', target_frame[:3, 3])

# ax = plot_utils.init_3d_figure() 
# left_arm_chain.plot(left_arm_chain.inverse_kinematics(target_frame), ax, target=target_vector, show=True) 

# Computed position vector: [ 0.1005863  -0.37787796 -0.06366723] Original position vector: [ 0.15180116 -0.60175085 -0.10976427]
# Computed position vector: [ 0.14025082  0.00242312 -0.36057011] Original position vector: [ 0.21335579  0.00382629 -0.57779678]