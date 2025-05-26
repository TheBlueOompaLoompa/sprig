#!/usr/bin/env bash
export AMPY_PORT=/dev/ttyACM0
export AMPY_BAUD=115200

script_dir=`dirname $0`

if [ ! -f $script_dir/venv/bin/activate ]; then
	echo No virtual environment detected!
	echo Attempting to create one
	python -m venv $script_dir/venv
	source $script_dir/venv/bin/activate
	pip install -r $script_dir/requirements.txt
else
	. $script_dir/venv/bin/activate
fi
