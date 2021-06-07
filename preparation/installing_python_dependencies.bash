#!/bin/bash

# run with: "bash installing_dependencies.bash"

PYTHONPATH="/usr/bin/python3.9"

$PYTHONPATH -m pip install --upgrade pip

# owslib 
$PYTHONPATH -m pip install OWSLib

# geopandas 
$PYTHONPATH -m pip install geopandas

# wget 
$PYTHONPATH -m pip install wget

# timeout-decorator 
$PYTHONPATH -m pip install timeout-decorator
