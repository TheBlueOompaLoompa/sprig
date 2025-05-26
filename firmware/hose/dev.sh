#!/usr/bin/env bash
source setup.sh
source venv/bin/activate
nodemon -w src -e py --exec ./compile.sh
