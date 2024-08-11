#!/usr/bin/env bash
source setup.sh
source bin/activate
nodemon -w src -e py --exec ./compile.sh
