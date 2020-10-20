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

        self.dir = 0 # 0:stop 1:foward 2:back 3:right 4:left 

        self.create_widgets()

        self.delay = 10 #[msec]
        self.update()


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
        self.btn_up.configure(width=15,height=1,command=self.press_up_button)
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

    def update(self):
        # KEY CHECK
        if self.dir== 0: # stop
            self.payload["right"]="brake"
            self.payload["left"]="brake"
        elif self.dir==1: # foward
            self.payload["right"]="forward"
            self.payload["left" ]="forward"
        elif self.dir==2: # back
            self.payload["right"]="back"
            self.payload["left" ]="back"
        elif self.dir==3: # right
            self.payload["right"]="back"
            self.payload["left" ]="forward"
        elif self.dir==4: # left
            self.payload["right"]="forward"
            self.payload["left" ]="back"
        else:
            self.payload["right"]="brake"
            self.payload["left"]="brake"
            

        # SEND REQUEST
        response = None
        r = requests.post( self.url, headers=self.headers, data=json.dumps(self.payload))

        # ACCEPT RESPONSE
        jsn = r.json()
        self.img = jsn["img"]
        if len(self.img) != 0:
            self.img = Image.open(io.BytesIO(base64.b64decode(self.img)))
            self.img = ImageTk.PhotoImage(self.img)

        # Draw Image
        self.canvas.create_image(0,0,image=self.img, anchor=tk.NW)

        self.master.after(self.delay, self.update)


    def press_up_button(self):
        self.dir = 1

    def press_back_button(self):
        self.dir = 2

    def press_right_button(self):
        self.dir = 3

    def press_left_button(self):
        self.dir = 4

    def press_stop_button(self):
        self.dir = 0

def main():
    root = tk.Tk()
    app = ClientApplication(master=root)
    app.mainloop()

if __name__ == '__main__':
    print("main")
    main()

