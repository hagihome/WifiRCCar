import tkinter as tk
from tkinter import ttk
import json
import requests
import io
from PIL import Image, ImageTk
import base64
import time

class ClientApplication( tk.Frame ):

    def __init__( self, master ):
        super().__init__(master)
        self.ip="192.168.1.13"
        self.port=8000
        self.url = "http://"+self.ip+":"+str(self.port)
        self.headers = {'content-type':'application/json'}
        self.payload = {"right":"none","left":"none","camera":"cap"}

        self.master.geometry("370x440")
        self.master.title("WifiRCCar Client Application")

        self.width = 320
        self.height= 240

        self.create_widgets()

        self.cur_key_state='brake'


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

        # Key Bind
        self.frame.bind("<KeyPress-w>", self.press_forward_key)
        self.frame.bind("<KeyPress-s>", self.press_back_key)
        self.frame.bind("<KeyPress-a>", self.press_left_key)
        self.frame.bind("<KeyPress-d>", self.press_right_key)
        self.frame.bind("<KeyRelease>", self.keyrelease)
        self.frame.focus_set()

    def press_forward_button(self):
        self.payload["right"]="forward"
        self.payload["left" ]="forward"
        response = None
        r = requests.post( self.url, headers=self.headers, data=json.dumps(self.payload))

    def press_back_button(self):
        self.payload["right"]="back"
        self.payload["left" ]="back"
        response = None
        r = requests.post( self.url, headers=self.headers, data=json.dumps(self.payload))

    def press_right_button(self):
        self.payload["right"]="back"
        self.payload["left" ]="forward"
        response = None
        r = requests.post( self.url, headers=self.headers, data=json.dumps(self.payload))

    def press_left_button(self):
        self.payload["right"]="forward"
        self.payload["left" ]="back"
        response = None
        r = requests.post( self.url, headers=self.headers, data=json.dumps(self.payload))

    def press_stop_button(self):
        self.payload["right"]="brake"
        self.payload["left"]="brake"
        response = None
        r = requests.post( self.url, headers=self.headers, data=json.dumps(self.payload))

    # ---- key control ----
    def press_forward_key(self, e):
        if (self.cur_key_state=='forward'): return
        self.cur_key_state = 'forward'
        self.payload["right"]="forward"
        self.payload["left" ]="forward"
        response = None
        r = requests.post( self.url, headers=self.headers, data=json.dumps(self.payload))

    def press_back_key(self,e):
        if (self.cur_key_state=='back'): return
        self.cur_key_state = 'back'
        self.payload["right"]="back"
        self.payload["left" ]="back"
        response = None
        r = requests.post( self.url, headers=self.headers, data=json.dumps(self.payload))

    def press_right_key(self, e):
        if (self.cur_key_state=='right'): return
        self.cur_key_state = 'right'
        self.payload["right"]="back"
        self.payload["left" ]="forward"
        response = None
        r = requests.post( self.url, headers=self.headers, data=json.dumps(self.payload))

    def press_left_key(self,e):
        if (self.cur_key_state=='left'): return
        self.cur_key_state = 'left'
        self.payload["right"]="forward"
        self.payload["left" ]="back"
        response = None
        r = requests.post( self.url, headers=self.headers, data=json.dumps(self.payload))

    def keyrelease(self, e):
        self.cur_key_state='brake'
        self.payload["right"]="brake"
        self.payload["left"]="brake"
        response = None
        r = requests.post( self.url, headers=self.headers, data=json.dumps(self.payload))

def main():
    root = tk.Tk()
    app = ClientApplication(master=root)
    app.mainloop()

if __name__ == '__main__':
    print("main")
    main()

