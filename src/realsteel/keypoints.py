import sys
import argparse
from openni import openni2, nite2, utils
import cv2
import numpy as np
import pprint
from multiprocessing import Process, Queue
import matplotlib.pyplot as plt

class Pose:
    """Pose estimation class using Kinect, OpenNI2, and NiTE2"""

    def __init__(self):        
        self.GRAY_COLOR = (64, 64, 64)
        self.CAPTURE_SIZE_KINECT = (512, 424)
        self.CAPTURE_SIZE_OTHERS = (640, 480)

    def init_capture_device(self):
        openni2.initialize()
        nite2.initialize('/usr/local/lib/')
        return openni2.Device.open_any()

    def close_capture_device(self):
        nite2.unload()
        openni2.unload()

    def joint_in_meters(self, j, ndigits=None):
        # OpenNI2.0 seems to return coordinates in right hand coordinate system
        # https://documentation.help/OpenNI-2.0/classopenni_1_1_coordinate_converter.html
        return (round(j.position.x/1000, ndigits), round(j.position.y/1000, ndigits), round(j.position.z/1000, ndigits)) if ndigits else \
                (j.position.x/1000, j.position.y/1000, j.position.z/1000)

    def get_joints(self, user):
        joints = {name: self.joint_in_meters(user.skeleton.joints[i]) for i, name in nite2.JointType._values_.items()}
        return joints

    def draw_limb(self, img, ut, j1, j2, col):
        (x1, y1) = ut.convert_joint_coordinates_to_depth(j1.position.x, j1.position.y, j1.position.z)
        (x2, y2) = ut.convert_joint_coordinates_to_depth(j2.position.x, j2.position.y, j2.position.z)

        if (0.4 < j1.positionConfidence and 0.4 < j2.positionConfidence):
            c = self.GRAY_COLOR if (j1.positionConfidence < 1.0 or j2.positionConfidence < 1.0) else col
            cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), c, 1)

            font = cv2.FONT_HERSHEY_SIMPLEX

            c = self.GRAY_COLOR if (j1.positionConfidence < 1.0) else col
            cv2.circle(img, (int(x1), int(y1)), 2, c, -1)
            cv2.putText(img, str(self.joint_in_meters(j1, 2)), (int(x1), int(y1)), font, .5, (255, 255, 255), 1, cv2.LINE_AA)

            c = self.GRAY_COLOR if (j2.positionConfidence < 1.0) else col
            cv2.circle(img, (int(x2), int(y2)), 2, c, -1)
            cv2.putText(img, str(self.joint_in_meters(j2, 2)), (int(x2), int(y2)), font, .5, (255, 255, 255), 1, cv2.LINE_AA)

    def draw_skeleton(self, img, ut, user, col):
        for idx1, idx2 in [(nite2.JointType.NITE_JOINT_HEAD, nite2.JointType.NITE_JOINT_NECK),
                        # upper body
                        (nite2.JointType.NITE_JOINT_NECK, nite2.JointType.NITE_JOINT_LEFT_SHOULDER),
                        (nite2.JointType.NITE_JOINT_LEFT_SHOULDER, nite2.JointType.NITE_JOINT_TORSO),
                        (nite2.JointType.NITE_JOINT_TORSO, nite2.JointType.NITE_JOINT_RIGHT_SHOULDER),
                        (nite2.JointType.NITE_JOINT_RIGHT_SHOULDER, nite2.JointType.NITE_JOINT_NECK),
                        # left hand
                        (nite2.JointType.NITE_JOINT_LEFT_HAND, nite2.JointType.NITE_JOINT_LEFT_ELBOW),
                        (nite2.JointType.NITE_JOINT_LEFT_ELBOW, nite2.JointType.NITE_JOINT_LEFT_SHOULDER),
                        # right hand
                        (nite2.JointType.NITE_JOINT_RIGHT_HAND, nite2.JointType.NITE_JOINT_RIGHT_ELBOW),
                        (nite2.JointType.NITE_JOINT_RIGHT_ELBOW, nite2.JointType.NITE_JOINT_RIGHT_SHOULDER),
                        # lower body
                        (nite2.JointType.NITE_JOINT_TORSO, nite2.JointType.NITE_JOINT_LEFT_HIP),
                        (nite2.JointType.NITE_JOINT_LEFT_HIP, nite2.JointType.NITE_JOINT_RIGHT_HIP),
                        (nite2.JointType.NITE_JOINT_RIGHT_HIP, nite2.JointType.NITE_JOINT_TORSO),
                        # left leg
                        (nite2.JointType.NITE_JOINT_LEFT_FOOT, nite2.JointType.NITE_JOINT_LEFT_KNEE),
                        (nite2.JointType.NITE_JOINT_LEFT_KNEE, nite2.JointType.NITE_JOINT_LEFT_HIP),
                        # right leg
                        (nite2.JointType.NITE_JOINT_RIGHT_FOOT, nite2.JointType.NITE_JOINT_RIGHT_KNEE),
                        (nite2.JointType.NITE_JOINT_RIGHT_KNEE, nite2.JointType.NITE_JOINT_RIGHT_HIP)]:
            self.draw_limb(img, ut, user.skeleton.joints[idx1], user.skeleton.joints[idx2], col)

    def launch(self, queue, DEBUG: bool=False):
        q = queue
        p = Process(target=self.runloop, args=(q, DEBUG))
        return p

    def runloop(self, queue: Queue, DEBUG: bool):
        """Start running the pose estimation

        Enqueue current frame's joint information

        Args:
            queue: Queue object to hold joint information
            DEBUG: when true displays depth frames with joints superimposed
        
        """
        # Setup Kinect, OpenNI2, NiTE2
        dev = self.init_capture_device()
        dev_name = dev.get_device_info().name.decode('UTF-8')
        print("Device Name: {}".format(dev_name))

        use_kinect = False
        if dev_name == 'Kinect':
            use_kinect = True
            print('using Kinect.')

        try:
            user_tracker = nite2.UserTracker(dev)
        except utils.NiteError:
            print("Unable to start the NiTE human tracker. Check "
                "the error messages in the console. Model data "
                "(s.dat, h.dat...) might be inaccessible.")
            sys.exit(-1)

        # Display window dimensions
        (img_w, img_h) = self.CAPTURE_SIZE_KINECT if use_kinect else self.CAPTURE_SIZE_OTHERS
        win_w = 1024
        win_h = int(img_h * win_w / img_w)

        while True:
            ut_frame = user_tracker.read_frame()

            depth_frame = ut_frame.get_depth_frame()
            depth_frame_data = depth_frame.get_buffer_as_uint16()
            img = np.ndarray((depth_frame.height, depth_frame.width), dtype=np.uint16,
                            buffer=depth_frame_data).astype(np.float32)
            if use_kinect:
                img = img[0:img_h, 0:img_w]

            (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(img)
            if (min_val < max_val):
                img = (img - min_val) / (max_val - min_val)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

            if ut_frame.users:
                # Get first person
                user = ut_frame.users[0]
                if user.is_new():
                    print("new human id:{} detected.".format(user.id))
                    user_tracker.start_skeleton_tracking(user.id)
                elif (user.state == nite2.UserState.NITE_USER_STATE_VISIBLE and
                    user.skeleton.state == nite2.SkeletonState.NITE_SKELETON_TRACKED):
                    # Build joint positions
                    joints = self.get_joints(user)
                    queue.put(joints)
                    
                    if DEBUG:
                        # Draw depth map and skeleton frame
                        self.draw_skeleton(img, user_tracker, user, (0, 255, 0))

            if DEBUG:
                # Draw coordinate system
                (o_x, o_y) = user_tracker.convert_joint_coordinates_to_depth(0, 0, 1)
                (x_x, x_y) = user_tracker.convert_joint_coordinates_to_depth(.1, 0, 1)
                (y_x, y_y) = user_tracker.convert_joint_coordinates_to_depth(0, .1, 1)
                cv2.line(img, (int(o_x), int(o_y)), (int(x_x), int(x_y)), (0, 0, 255), 1)
                cv2.line(img, (int(o_x), int(o_y)), (int(y_x), int(y_y)), (0, 255, 0), 1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, str((.1, 0)), (int(x_x), int(x_y)), font, .5, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(img, str((0, .1)), (int(y_x), int(y_y)), font, .5, (255, 255, 255), 1, cv2.LINE_AA)

                cv2.imshow("Depth", cv2.resize(img, (win_w, win_h)))
                if (cv2.waitKey(1) & 0xFF == ord('q')):
                    plt.close()
                    break

        self.close_capture_device()

if __name__ == '__main__':
    joints = Queue(maxsize=3)
    keypoints_proc = Pose().launch(joints, DEBUG=True)
    
    print('Starting pose detection process')

    keypoints_proc.start()

    while True:
        # Get most recent joints point cloud
        if not joints.empty():
            jointsFrame = joints.get()
            pprint.pprint(jointsFrame['NITE_JOINT_RIGHT_HAND'])
            pprint.pprint(jointsFrame['NITE_JOINT_RIGHT_SHOULDER'])
        
        if not keypoints_proc.is_alive():
            print('Pose detection process killed')
            break
