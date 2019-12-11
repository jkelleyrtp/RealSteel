import os
import sys
import argparse
import time
import freenect
import cv2
import numpy as np
import pprint
from multiprocessing import Process, Queue

class Pose:
    """Pose estimation class bridging OpenPose and Kinect

    Args:
        params: OpenPose custom params (refer to OpenPose include/openpose/flags.hpp for more parameters)
        camera: kinect camera device index (default: 0)
        model_path: path to OpenPose models installed directory (default: models/)
    """

    def __init__(self, params: dict={}, camera: int=0, model_path: str='/home/richard/Desktop/openpose/models/'):
        try:
            sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
            self.op = op
        except ImportError as e:
            print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` \
                in CMake and have this Python script in the right folder?')
            raise e

        if not params:
            # Set default parameters for Olin laptops
            params["net_resolution"] = "-1x160"
            params["model_pose"] = "COCO"
            params["tracking"] = "1"
            params["number_people_max"] = "1"
            params["part_candidates"] = True
        
        self.params = params

        # Add model path
        self.params["model_folder"] = model_path

        self.camera = camera

    def get_video(self) -> np.ndarray:
        """Get RGB image from the kinect
        
        Returns:
            numpy array of RGB image

        """
        array, _ = freenect.sync_get_video()
        array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
        array = cv2.flip(array, 1)
        return array
    
    def get_depth(self, format=freenect.DEPTH_REGISTERED) -> np.ndarray:
        """Get depth from the kinect
        
        Args:
            format: kinect depth format (default: DEPTH_REGISTERED,
            produces distance in millimeters where (x,y) of depth matches (x,y) of video)
                
        Returns:
            numpy array of depth image

        """
        array, _ = freenect.sync_get_depth(format=format)
        return array

    def jointPoints(self, keypoints, depths: np.ndarray, confidenceThreshold: int=.6) -> dict:
        """Determine joint point cloud

        Args:
            keypoints: OpenPose posecandidates keypoints
            depths: depth image
            confidenceThreshold: any joint above this value is considered (default: .6) 

        Returns:
            dict of joint dictonaries with point cloud (meters) and image coordinates

        """
        COCO_OUTPUT = ['Nose', 'Neck', 'Rsho', 'Relb', 'Rwri', 'Lsho', 'Lelb', 'Lwri','Rhip',\
            'Rkne', 'Rank', 'Lhip', 'Lkne', 'Lank', 'Leye', 'Reye', 'Lear', 'Rear']
        joints = {}
        for idx, joint in enumerate(np.asarray(keypoints)):
            coords = np.asarray(joint[0][0:2]).astype(int) \
                if len(joint) > 0 and joint[0][2] > confidenceThreshold else []
            
            # Ignore empty joints
            if not len(coords):
                joints[COCO_OUTPUT[idx]] = {}
                continue

            # Known openpose bug where it predicts outside frame dimensions
            if coords[0] > 640 and coords[1] > 480:
                print('DEBUG: Openpose predicted joint out of frame')
                joints[COCO_OUTPUT[idx]] = {}
                continue
            
            # Numpy array order is row, col -> y, x
            wz = depths[coords[1], coords[0]]

            # Ignore joints not in depth thresholds
            if wz == 0:
                joints[COCO_OUTPUT[idx]] = {}
                continue
            
            # Get x and y in world coordinates in mm
            wx, wy = freenect.camera_to_world(coords[0], coords[1], wz, self.camera)
            joints[COCO_OUTPUT[idx]] = {'pc': (round(wx/1000, 2), round(wy/1000, 2), wz/1000), 'xy': (coords[0], coords[1])}
        
        return joints

    def launch(self, queue, DEBUG: bool=False):
        q = queue
        p = Process(target=self.runloop, args=(q, DEBUG))
        return p

    def runloop(self, queue: Queue, DEBUG: bool):
        """Start running the pose estimation

        Enqueue current frame's joint information

        Args:
            queue: Queue object to hold joint information
            DEBUG: when true displays kinect RGB and Depth frames with joints superimposed
        
        """
        # Starting OpenPose
        opWrapper = self.op.WrapperPython()
        opWrapper.configure(self.params)
        opWrapper.start()

        while True:
            img = self.get_video()

            # Process Image
            datum = self.op.Datum()
            datum.cvInputData = img
            opWrapper.emplaceAndPop([datum])

            keypoints = datum.poseCandidates

            depths = self.get_depth()

            joints = self.jointPoints(keypoints, depths)
            queue.put(joints)

            if DEBUG:
                # Render OpenPose frame
                im = datum.cvOutputData

                # Display joint values
                font = cv2.FONT_HERSHEY_SIMPLEX
                for name, joint in joints.items():
                    if joint:
                        cv2.putText(im, str(joint['pc']), joint['xy'], font, .5, (0, 255, 0), 1, cv2.LINE_AA)
                
                cv2.imshow('Pose Estimation', im)
                cv2.imshow('Depth image', depths.astype(np.uint8))

                key = cv2.waitKey(1)
                if key == ord('q'):
                    break 
        
        if DEBUG:
            cv2.destroyAllWindows()

if __name__ == '__main__':
    joints = Queue()
    keypoints_proc = Pose().launch(joints, DEBUG=False)
    
    print('Starting pose detection process')

    keypoints_proc.start()

    while True:
        # Get most recent joints point cloud
        if not joints.empty():
            jointsFrame = joints.get()
            pprint.pprint(jointsFrame)
        
        if not keypoints_proc.is_alive():
            print('Pose detection process killed')
            break
