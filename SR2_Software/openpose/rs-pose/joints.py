import sys
import cv2
import os
from sys import platform
import argparse
import pprint
import time

def main():
    try:
        sys.path.append('../build/python')
        from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Flags
    parser = argparse.ArgumentParser()
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../models/"

    # Set default parameters for Olin laptops
    params["net_resolution"] = "-1x160"
    params["model_pose"] = "COCO"
    params["tracking"] = "1"
    params["number_people_max"] = "1"
    params["part_candidates"] = True

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    stream = cv2.VideoCapture(0)

    font = cv2.FONT_HERSHEY_SIMPLEX

    num_frames = 0
    fps = '-'

    while True:
        if not num_frames:
            start = time.time()

        ret, img = stream.read()
        img = cv2.flip(img, 1)

        # Process Image
        datum = op.Datum()
        datum.cvInputData = img
        opWrapper.emplaceAndPop([datum])

        keypoints = datum.poseCandidates

        # Print the human pose keypoints, i.e., a [#people x #keypoints x 3]-dimensional numpy object with the keypoints of all the people on that image
        if len(keypoints) > 0:
            print('Human(s) Pose Estimated!')
            pprint.pprint(keypoints)
        else:
            print('No humans detected!')

        # Caclulate FPS
        num_frames += 1
        if num_frames >= 10:
            end = time.time()
            fps = round(num_frames / (end - start), 2)
            num_frames = 0

        # Render frame
        im = datum.cvOutputData
        cv2.putText(im, 'FPS: ' + str(fps), (10, 30), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow('Pose Estimation', im)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break 


    stream.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()