# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import pprint

try:
    try:
        sys.path.append('../build/python');
        from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", default="./hugh.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../models/"

    #Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item

    # Set default parameters for Olin laptops
    if "net_resolution" not in params:
        params["net_resolution"] = "-1x160"
    if "model_pose" not in params:
        params["model_pose"] = "COCO"
    params["part_candidates"] = True


    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Process Image
    datum = op.Datum()
    imageToProcess = cv2.imread(args[0].image_path)
    datum.cvInputData = imageToProcess
    opWrapper.emplaceAndPop([datum])

    # Display Image
    # print("Body keypoints: \n" + str(datum.poseKeypoints))
    pprint.pprint(datum.poseCandidates)
    print(len(datum.poseCandidates))
    cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", datum.cvOutputData)
    cv2.waitKey(0)

except Exception as e:
    print(e)
    sys.exit(-1)