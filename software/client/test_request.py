import argparse
import json
import requests
from time import sleep
import io
from PIL import Image
import base64

ip="192.168.1.9"
port=8000

CTRL_C = 3
KEY_A  = 97
KEY_B  = 98
KEY_C  = 99
KEY_D  = 100 
KEY_S  = 115
KEY_W  = 119

def getch():
    import sys
    import tty
    import termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd,termios.TCSADRAIN, old)

def send_request(url,payload):
    response = None
    headers = {'content-type':'application/json'}
    r = requests.post(url,headers=headers,data=json.dumps(payload))
    jsn = r.json()
    img = jsn["img"]
    if len(img) != 0:
        img = base64.b64decode(img)
        img = io.BytesIO(img)
        img = Image.open(img)
        img.save('sample.png')

def handle_keyevent(url):
    response = None
    header = {'content-type':'application/json'}
    
    while True:
        try:
            key = ord(getch())
            if key == CTRL_C:
                break
            print(key)

            if key == KEY_W:
                payload = {"right":"forward","left":"forward", "camera":"none"}
                send_request( url, payload)
            if key == KEY_S:
                payload = {"right":"back","left":"back", "camera":"none"}
                send_request( url, payload)
            if key == KEY_A:
                payload = {"right":"forward","left":"back", "camera":"none"}
                send_request( url, payload)
            if key == KEY_D:
                payload = {"right":"back","left":"forward", "camera":"none"}
                send_request( url, payload)
            if key == KEY_B:
                payload = {"right":"brake","left":"brake", "camera":"none"}
                send_request( url, payload)
            if key == KEY_C:
                payload = {"right":"none","left":"none","camera":"cap"}
                send_request( url, payload)
        except ValueError:
            print("Exception")


def main():
    parser = argparse.ArgumentParser("client_parser")
    parser.add_argument('--server_name', '-s', required=False, default='localhost')
    parser.add_argument('--port', '-p', required=False, default=8000)
    args = parser.parse_args()
    url = "http://"+str(args.server_name)+":"+str(args.port)
    print(url)
    handle_keyevent(url)

if __name__=='__main__':
    main()

