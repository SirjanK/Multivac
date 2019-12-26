#!/bin/bash

# Call this bash file with the following arguments:
#  i) Path to monkeyrunner executable
#  ii) Path to redispy lib

monkeyrunner_path=$1
redispy_path=$2

export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Test eventobjects
echo "Running test_eventobjects using python3"
python test/test_eventobjects.py

echo "ALL TESTS HAVE RUN"
