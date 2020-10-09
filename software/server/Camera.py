#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import picamera

class Camera:
  def __init__(self, name, reso_x, reso_y):
    self.name = name
    self.camera = picamera.PiCamera()
    self.camera.exposure_mode = 'auto'
    self.camera.meter_mode = 'matrix'
    self.camera.rotation = 180
    self.camera.resolution = (reso_x, reso_y)

  def capture(self):
    my_stream = io.BytesIO()
    self.camera.capture(my_stream, 'jpeg', use_video_port=True)
    return my_stream
