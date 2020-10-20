#!/bin/bash
#sudo pigpiod
ip=`hostname -I | awk '{print $1}'`
#ip=raspberypi.local

sport=8759
cport=8000
echo 'server https://'$ip
echo 'streaming server port : '$sport
echo 'control server port : '$cport

python3 stream_server.py -p $sport &
s_pid=$!
python3 http_server_without_cam.py -p $cport

kill $s_pid
