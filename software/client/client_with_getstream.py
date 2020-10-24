import tkinter as tk
from tkinter import ttk
import json
import requests
import io
from PIL import Image, ImageTk
import base64
import time

import cv2
import numpy as np
import urllib.request
import threading
import multiprocessing
import queue

import os

class ClientApplication( tk.Frame ):

    def __init__( self, master ):
        super().__init__(master)
        self.ip="192.168.1.13"
        self.cport=8000
        self.sport=8759
        self.url = "http://"+self.ip+":"+str(self.cport)
        self.headers = {'content-type':'application/json'}
        self.payload = {"right":"none","left":"none"}

        self.master.geometry("370x440")
        self.master.title("WifiRCCar Client Application")

        self.width = 320
        self.height= 240

        self.create_widgets()

        self.cur_key_max_cnt = 30
        self.cur_key_cnt  = 0
        self.cur_key_state='brake'

        self.stream_queue = multiprocessing.Manager().Queue(maxsize=1)
        self.thread_stop  = multiprocessing.Event()
        #self.stream_thread = threading.Thread(target=self.streaming)
        #self.stream_thread.setDaemon(True)
        self.stream_thread = multiprocessing.Process(target=self.streaming, args=(self.stream_queue,self.thread_stop))
        self.stream_thread.start()

        self.control_queue = multiprocessing.Manager().Queue()
        self.control_thread = multiprocessing.Process(target=self.send_control, args=(self.control_queue,self.thread_stop))
        self.control_thread.start()

        self.canvas_update()

    def create_widgets(self):
        self.frame = tk.LabelFrame( self.master, text='image' )
        self.frame.place(x=10,y=10)
        self.frame.configure(width = self.width+30, height=self.height+50)
        self.frame.grid_propagate(0)

        # Canvas
        self.canvas = tk.Canvas(self.frame)
        self.canvas.configure(width=self.width, height=self.height)
        self.canvas.grid(column=0,row=0,padx=10,pady=10)

        # Button
        self.area_btn = tk.LabelFrame( self.master, text='Control')
        self.area_btn.place( x=10, y=310 )
        self.area_btn.configure( width=self.width+30, height=120)
        self.area_btn.grid_propagate(0)

        self.btn_up = tk.Button( self.area_btn, text='UP')
        self.btn_up.configure(width=15,height=1,command=self.press_forward_button)
        self.btn_up.grid(column=2, row=1)

        self.btn_down = tk.Button( self.area_btn, text='DOWN')
        self.btn_down.configure(width=15,height=1,command=self.press_back_button)
        self.btn_down.grid(column=2, row=3)
        
        self.btn_left = tk.Button( self.area_btn, text='LEFT')
        self.btn_left.configure(width=15,height=1,command=self.press_left_button)
        self.btn_left.grid(column=1, row=2)
        
        self.btn_right = tk.Button( self.area_btn, text='RIGHT')
        self.btn_right.configure(width=15,height=1,command=self.press_right_button)
        self.btn_right.grid(column=3, row=2)
        
        self.btn_stop = tk.Button( self.area_btn, text='STOP')
        self.btn_stop.configure(width=15,height=1,command=self.press_stop_button)
        self.btn_stop.grid(column=2, row=2)

        # Event Bind
        self.master.protocol("WM_DELETE_WINDOW",self.close_window)

        # Key Bind
        self.frame.bind("<KeyPress-w>", self.press_forward_key)
        self.frame.bind("<KeyPress-s>", self.press_back_key)
        self.frame.bind("<KeyPress-a>", self.press_left_key)
        self.frame.bind("<KeyPress-d>", self.press_right_key)
        self.frame.bind("<KeyRelease>", self.keyrelease)
        self.frame.focus_set()

    # Protocol Control
    def close_window(self):
        print("close_window called")
        self.thread_stop.set()
        print("waiting thread closed")
        #self.stream_thread.join()
        while self.stream_thread.is_alive():
            print("thread is alived. join")
            self.stream_thread.join()
            time.sleep(0.1)
        print("destroy window")
        self.master.destroy()
        print("application finished")

    # Button Control
    def press_forward_button(self):
        self.payload["right"]="forward"
        self.payload["left" ]="forward"
        self.control_queue.put_nowait(self.payload)

    def press_back_button(self):
        self.payload["right"]="back"
        self.payload["left" ]="back"
        self.control_queue.put_nowait(self.payload)

    def press_right_button(self):
        self.payload["right"]="back"
        self.payload["left" ]="forward"
        self.control_queue.put_nowait(self.payload)

    def press_left_button(self):
        self.payload["right"]="forward"
        self.payload["left" ]="back"
        self.control_queue.put_nowait(self.payload)

    def press_stop_button(self):
        self.payload["right"]="brake"
        self.payload["left"]="brake"
        self.control_queue.put_nowait(self.payload)

    # ---- key control ----
    def press_forward_key(self, e):
        print('forward key pressed:',self.cur_key_state,":",self.cur_key_cnt)
        if (self.cur_key_state=='forward' and self.cur_key_cnt<self.cur_key_max_cnt):
            self.cur_key_cnt = self.cur_key_cnt+1
            return
        self.cur_key_cnt   = 0
        self.cur_key_state = 'forward'
        self.payload["right"]="forward"
        self.payload["left" ]="forward"
        self.control_queue.put_nowait(self.payload)

    def press_back_key(self,e):
        if (self.cur_key_state=='back' and self.cur_key_cnt<self.cur_key_max_cnt):
            self.cur_key_cnt = self.cur_key_cnt+1
            return
        self.cur_key_cnt   = 0
        self.cur_key_state = 'back'
        self.payload["right"]="back"
        self.payload["left" ]="back"
        self.control_queue.put_nowait(self.payload)

    def press_right_key(self, e):
        if (self.cur_key_state=='right' and self.cur_key_cnt<self.cur_key_max_cnt):
            self.cur_key_cnt = self.cur_key_cnt+1
            return
        self.cur_key_cnt   = 0
        self.cur_key_state = 'right'
        self.payload["right"]="back"
        self.payload["left" ]="forward"
        self.control_queue.put_nowait(self.payload)

    def press_left_key(self,e):
        if (self.cur_key_state=='left' and self.cur_key_cnt<self.cur_key_max_cnt):
            self.cur_key_cnt = self.cur_key_cnt+1
            return
        self.cur_key_cnt   = 0
        self.cur_key_state = 'left'
        self.payload["right"]="forward"
        self.payload["left" ]="back"
        self.control_queue.put_nowait(self.payload)

    def keyrelease(self, e):
        print('key released:',self.cur_key_state,":",self.cur_key_cnt)
        self.cur_key_cnt   = 0
        self.cur_key_state = 'brake'
        self.payload["right"]="brake"
        self.payload["left"]="brake"
        self.control_queue.put_nowait(self.payload)

    # --------------------------
    def streaming(self,q, e):
        bytes = b''
        url = "http://"+self.ip+":"+str(self.sport)+"/stream.mjpg"
        stream = urllib.request.urlopen(url=url)
        while True :
            if e.is_set():
                break
            #print("get stream")
            bytes += stream.read(1024)
            #print("proc stream")
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a!=-1 and b!=-1:
                jpg = bytes[a:b+2]
                bytes = bytes[b+2:]
                img = cv2.cvtColor(cv2.imdecode(np.fromstring(jpg,dtype=np.uint8),cv2.IMREAD_COLOR),cv2.COLOR_BGR2RGB)
                #img = ImageTk.PhotoImage(Image.fromarray(img))
                #self.canvas.create_image( 0, 0, image=img, anchor=tk.NW)
                try:
                    q.put_nowait(img)
                except queue.Full:
                    print("queue is full")
                    pass
        stream.close()
        print("thread closed")

    def send_control( self, q, e):
        while True :
            if e.is_set():
                break
            try :
                payload = q.get_nowait()
                print("payload:",payload)
                requests.post ( self.url, headers=self.headers, data=json.dumps(payload))
            except queue.Empty :
                pass
        print("send_control closed")

    # -----------------------------
    def canvas_update(self,):
        try:
            self.img = self.stream_queue.get_nowait()
            self.img = ImageTk.PhotoImage(Image.fromarray(self.img))
            self.canvas.create_image( 0, 0, image=self.img, anchor=tk.NW)
        except queue.Empty:
            print("queue is empty")
            pass
        self.master.after(33, self.canvas_update) # 15fps:66

def main():
    os.system('xset r off')
    root = tk.Tk()
    app = ClientApplication(master=root)
    app.mainloop()
    os.system('xset r on')

if __name__ == '__main__':
    print("main")
    main()

