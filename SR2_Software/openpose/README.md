# Instructions 

## Prerequisites

* [Docker](https://docs.docker.com/v17.12/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [nvidia-docker](https://github.com/NVIDIA/nvidia-docker#quickstart)


## Creating the container for the first time
cd into openpose directory containing docker-compose.yml

To create contianer and start openpose service in bash, run:

`docker-compose run --name openpose-realsteel openpose /bin/bash`

## Running the container

To start conainter: 

`docker start -i openpose-realsteel`

## Common commands
List all containers: `docker ps -a`

Remove all containers: `docker rm $(docker ps -a -q)`

## Common Errors

### Cannot connect to X server
Make sure you ran `xhost +` in host bash so that access control disabled and clients can connect from any host.

### X Error: BadShmSeg (invalid shared segment parameter)
Make sure that the environmental flag `QT_X11_NO_MITSHM=1` is set in docker-compose.yml

### Check failed: error == cudaSuccess (2 vs. 0)  out of memory
Reduce `net_resolution` flag to use less memory until error dissappears.

# Helpful Openpose Documentation

Here are a couple links that are helpful for using the openpose python API.

GitHub Repo: https://github.com/CMU-Perceptual-Computing-Lab/openpose

Python API Examples: https://github.com/CMU-Perceptual-Computing-Lab/openpose/tree/master/examples/tutorial_api_python

OpenPose Python Module & Demo: https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/modules/python_module.md

Python API Definitions: https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/python/openpose/openpose_python.cpp

OpenPose Output Format: https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/output.md

OpenPose Flags: https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/include/openpose/flags.hpp

