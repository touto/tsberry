#!/usr/bin/env python

import RPi.GPIO as GPIO
import threading
from time import sleep
import datetime
import smbus

class Encoder:
   'Common base class for all quadrature encoders'
   encCount = 0
   Counter = 0
   Tmp = 0
   global last_tick
   last_tick = 0
   def __enter__(self):
      print('__enter__ called')
      return self

   def __exit__(self, *a):
      print('__exit__ called')

   def __init__(self, pin_a, pin_b, debounce=0, name=""):
      self.pin_a = pin_a
      self.pin_b = pin_b
      self.name = name
      self.debounce = debounce
      Encoder.encCount += 1

      GPIO.setup(pin_a, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
      GPIO.setup(pin_b, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)
      if debounce:
         print "debounce on"
         GPIO.add_event_detect(pin_a, GPIO.BOTH, callback=self.interrupt_both, bouncetime=debounce)
         GPIO.add_event_detect(pin_b, GPIO.BOTH, callback=self.interrupt_both, bouncetime=debounce)
      else:
         print "debounce off"
         GPIO.add_event_detect(pin_a, GPIO.BOTH, callback=self.interrupt_both)
         GPIO.add_event_detect(pin_b, GPIO.BOTH, callback=self.interrupt_both)
         

   def mapNumber(self, number):
      if number < 1:
         self.Counter = 0
         return 0
      elif number > 254:
         self.Counter = 255
         return 255
      else:
         self.Counter = number
         return number
 
   def displayCount(self):
     print "Total Encoders %d" % Encoder.encCount

   def displayName(self):
     return self.name

   def displayEncoder(self):
      print "Pin A : ", self.pin_a,  ", Pin B: ", self.pin_b, ", Debounce: ", self.debounce

   def interrupt_both(self, arg):
      #print arg2
      global Counter
      global Tmp
      global last_tick
      #divider = float(10000)

      #current_tick = datetime.datetime.now()

      #tick = current_tick - last_tick

      #multiplier = (1 / float (tick.microseconds / divider))
      #print "\n"
      #if tick.microseconds < 8853:
      #   print "fast"
      #else:
      #   print "slow"

      if arg == self.pin_a:

         a = datetime.datetime.now()

         if GPIO.input(self.pin_a)^GPIO.input(self.pin_b):
            self.Tmp += 1
         else:
            self.Tmp -= 1

      elif arg == self.pin_b:

         if GPIO.input(self.pin_a)^GPIO.input(self.pin_b):
            self.Tmp -= 1
         else:
            self.Tmp += 1

      #if multiplier < 1:
      #   multiplier = 1
      #print "___________\n"
      #print int(multiplier)
      #print "___________\n"
      #print int((Tmp)/4)
      #self.last_tick = datetime.datetime.now()

      if self.Tmp > 2:
            self.Counter += 1
            self.mapNumber(self.Counter)
            I2C().sendRGBW(encRed.Counter, encGreen.Counter, encBlue.Counter, encWhite.Counter)
            #print "%s: %s" % (self.displayName(), self.Counter)
            self.Tmp = 0

      elif self.Tmp < -2:
            self.Counter -= 1
            self.mapNumber(self.Counter)
            I2C().sendRGBW(encRed.Counter, encGreen.Counter, encBlue.Counter, encWhite.Counter)
            #print "%s: %s" % (self.displayName(), self.Counter)
            self.Tmp = 0

class I2C:
   'I2C com class'
   bus = smbus.SMBus(1)
   address = 0x04
   def writeNumber(self, value):
      bus.write_byte(address, value)
      print "write"
      # bus.write_byte_data(address, 0, value)
      return -1

   def readNumber(self):
      number = bus.read_byte(address)
      # number = bus.read_byte_data(address, 1)
      return number

   def sendRGBW(self, r, g, b, w):
      self.bus.write_byte(self.address, r)
      self.bus.write_byte(self.address, g)
      self.bus.write_byte(self.address, b)
      self.bus.write_byte(self.address, w)
      #print "_____"
      #print r
      #print g
      #print b
      #print w
      #print "____"

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

encRed = Encoder(4, 14, 15, "red")
encGreen = Encoder(17, 18, 15, "green")
encBlue = Encoder(22, 23, 15, "bluew")
encWhite = Encoder(24, 25, 15, "white")


#"This would create second object of Employee class"
#enc2 = Encoder(5, 15)
encRed.displayEncoder()
encGreen.displayEncoder()
encBlue.displayEncoder()
encWhite.displayEncoder()

#enc2.displayEncoder()
while True:
   #I2C().sendRGBW(encRed.Counter, encGreen.Counter, encBlue.Counter, encWhite.Counter)
   sleep (1)
