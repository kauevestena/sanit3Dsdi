# #!/bin/bash

# # run with: "bash pymesh_install.bash"
# # please run iN yout HOME FOLDER

# # test aliasing: https://askubuntu.com/questions/320996/how-to-make-python-program-command-execute-python-3

# # PYTHONPATH="python3.8"

# # alias python=python3.8

# sudo apt-get install \
#     libeigen3-dev \
#     libgmp-dev \
#     libgmpxx4ldbl \
#     libmpfr-dev \
#     libboost-dev \
#     libboost-thread-dev \
#     libtbb-dev \
#     python3-dev


# git clone https://github.com/PyMesh/PyMesh.git
# cd PyMesh
# git submodule update --init
# export PYMESH_PATH='pwd'

# # $PYTHONPATH -m pip install -r $PYMESH_PATH/python/requirements.txt
# python -m pip install -r $PYMESH_PATH/python/requirements.txt


# ./setup.pyhttps://github.com/PyMesh/PyMesh/releases/download/v0.3/pymesh2-0.3-cp37-cp37m-linux_x86_64.whl build

# sudo ./setup.py install

# # verify installation:

# python -c "import pymesh; pymesh.test()"

wget https://github.com/PyMesh/PyMesh/releases/download/v0.3/pymesh2-0.3-cp37-cp37m-linux_x86_64.whl

python3.7 -m pip install numpy

python3.7 -m pip install pymesh2-0.3-cp37-cp37m-linux_x86_64.whl

