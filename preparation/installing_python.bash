#!/bin/bash

# run with: "bash installing_python.bash"

PYHON_VER=3.7

#installing python 3.7
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python$PYHON_VER