# This module takes in raw input devices and produces the raw angles
from multiprocessing import Process, Queue
from realsteel.keypoints import Pose
import time

class JOINT_INPUT:
    def __init__(self, *args, **kwargs):
        pass

class CAMERA(JOINT_INPUT):
    """
    Sets up the camera-only pipeline
    """
    def __init__(self, *args, **kwargs):
        pass

class KINECT(JOINT_INPUT):
    """
    Sets up the kinect-only pipeline
    """
    def __init__(self, *args, **kwargs):
        pass

class HYBRID(JOINT_INPUT):
    """
    Sets up the hybrid pipeline
    """
    def __init__(self, *args, **kwargs):
        pass

    def launch(self, queue):
        q = queue
        p = Process(target=self.main_loop, args=(q,))
        return p

    def main_loop(self, queue: Queue):
        keypoints_proc = Pose().launch(queue, DEBUG=True)
        keypoints_proc.start()

        # i = [0, 0]
        # while True:
        #     time.sleep(.00025)
        #     i[0] += .01
        #     i[1] += .01
        #     queue.put(i)
        # try:
        #     sys.path.append('/usr/local/python')
        #     from openpose import pyopenpose as op
        # except ImportError as e:
        #     print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        #     raise e

        # # Flags
        # parser = argparse.ArgumentParser()
        # args = parser.parse_known_args()

        # # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        # params = dict()
        # params["model_folder"] = "/home/richard/Desktop/openpose/models/"

        # # Set default parameters for Olin laptops
        # params["net_resolution"] = "-1x160"
        # params["model_pose"] = "COCO"
        # # params["tracking"] = "1"
        # params["number_people_max"] = "1"
        # params["part_candidates"] = True

        # # Starting OpenPose
        # opWrapper = op.WrapperPython()
        # opWrapper.configure(params)
        # opWrapper.start()

        # cv2.namedWindow('Pose Estimation')

        # while True:
        #     if not num_frames:
        #         start = time.time()

        #     img = freenect.sync_get_video()[0]
        #     img = cv2.flip(img, 1)

        #     # Process Image
        #     datum = op.Datum()
        #     datum.cvInputData = img
        #     opWrapper.emplaceAndPop([datum])

        #     keypoints = datum.poseCandidates

        #     # points of interest
        #     pos = [1, 2, 3, 4, 5, 6, 7]

        #     joints = {}
        #     for idx, i in enumerate(np.asarray(keypoints)[pos]):
        #         if i:
        #             if idx == 0:
        #                 joints['neck'] = [int(j) for j in i[0][0:2]]
        #             if idx == 1:
        #                 joints['left-shoulder'] = [int(j) for j in i[0][0:2]]
        #             if idx == 2:
        #                 joints['left-elbow'] = [int(j) for j in i[0][0:2]]
        #             if idx == 3:
        #                 joints['left-wrist'] = [int(j) for j in i[0][0:2]]
        #             if idx == 4:
        #                 joints['right-shoulder'] = [int(j) for j in i[0][0:2]]
        #             if idx == 5:
        #                 joints['right-elbow'] = [int(j) for j in i[0][0:2]]
        #             if idx == 6:
        #                 joints['right-wrist'] = [int(j) for j in i[0][0:2]]
            

        #     # Get depth information from kinect in world coordinates
        #     array,_ = freenect.sync_get_depth(format=freenect.DEPTH_REGISTERED)
        #     array = array.astype(np.uint8)

        #     # Convert x, y in to world coordinates using depth as reference
        #     if 'left-wrist' in joints:
        #         wrist = joints['left-wrist']
        #         if wrist[0] > 640 and wrist[1] > 480:
        #             print('Openpose predicted joint out of frame')
        #             continue

        #         # Get depth at joint keypoint given by openpose
        #         d = array[wrist[1], wrist[0]]

        #         # Ignore when depth is 0 -> joint is too too close to camera, less than minimum threshold
        #         if not d:
        #             print('Joint too close, Depth: ', d)
        #             continue

        #         wx, wy = freenect.camera_to_world(wrist[0], wrist[1], d)

        #         print('(x,y,z): ', wx, wy, d)
        #     else:
        #         print('Joint not in frame')

        #     # Render frame
        #     im = datum.cvOutputData
        #     cv2.imshow('Pose Estimation', im)

        #     key = cv2.waitKey(1)
        #     if key == ord('q'):
        #         break 

        # cv2.destroyAllWindows()