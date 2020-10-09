#!/bin/bash
sudo pigpiod
ip=`hostname -I | awk '{print $1}'`
#ip=raspberypi.local
port=8000
echo 'server https://'$ip':'$port
python3  http_server.py -s $ip -p $port

