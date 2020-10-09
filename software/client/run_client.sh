#!/bin/bash

export SDL_FBDEV=/dev/fb0
#ip=raspberrypi.local
ip=192.168.1.23
port=8000

python3 test_request.py -s $ip -p $port
