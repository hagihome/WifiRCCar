#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pigpio

class Motor:
  def __init__(self, name, pin1, pin2):
    self.name = name
    self.gpio = pigpio.pi()
    self.pin1 = pin1
    self.pin2 = pin2
    self.gpio.set_mode( self.pin1, pigpio.OUTPUT)
    self.gpio.set_mode( self.pin2, pigpio.OUTPUT)

  def forward(self):
    print("{} forward".format(self.name))
    self.gpio.write( self.pin1, 1)
    self.gpio.write( self.pin2, 0)

  def back(self):
    print("{} back".format(self.name))
    self.gpio.write( self.pin1, 0)
    self.gpio.write( self.pin2, 1)

  def brake(self):
    print("{} brake".format(self.name))
    self.gpio.write( self.pin1, 0)
    self.gpio.write( self.pin2, 0)

  def cleanup(self):
    print("{} cleanup".format(self.name))
    self.gpio.set_mode( self.pin1, pigpio.INPUT)
    self.gpio.set_mode( self.pin2, pigpio.INPUT)

from time import sleep
def main():
  left = Motor("Left", 20, 21)
  right= Motor("Right", 26, 19)
  sleep(2)
  left.forward()
  right.forward()
  sleep(2)
  left.back()
  right.back()
  sleep(2)
  left.forward()
  right.back()
  sleep(2)
  left.back()
  right.forward()
  sleep(2)
  left.brake()
  right.brake()
  


if __name__ == '__main__':
  main()

