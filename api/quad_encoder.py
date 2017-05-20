#!/usr/bin/env python

import RPi.GPIO as GPIO
import threading
from time import sleep
import datetime
import requests

session = requests.Session()

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

   def __init__(self, pin_a, pin_b, debounce=0, name="", controller=""):
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
            #I2C().sendRGBW(encRed.Counter, encGreen.Counter, encBlue.Counter, encWhite.Counter)
            try:
                manual_controll.update("manual_controll")
                pass
            except requests.exceptions.ConnectionError:
               print "connection error"
            print "%s: %s" % (self.displayName(), self.Counter)
            self.Tmp = 0

      elif self.Tmp < -2:
            self.Counter -= 1
            self.mapNumber(self.Counter)
            try:
               manual_controll.update("manual_controll")
            except requests.exceptions.ConnectionError:
               print "connection error"

            print "%s: %s" % (self.displayName(), self.Counter)
            self.Tmp = 0

class Controller:
    name = "controller 1"
    encoders = []

    def addEncoder(self, *encoders):
        for encoder in encoders:
            self.encoders.append(encoder)

    def listEncoders(self):
        for encoder in self.encoders:
            pass
            print encoder.displayName()
        return True

    def currentValues(self):
        currentValues = {}
        for encoder in self.encoders:
            currentValues[encoder.name] = encoder.Counter
        return currentValues

    def update(self, controller):
        currentValues = self.currentValues()
        print currentValues['red']
        try:
            session.patch('http://127.0.0.1/api/areas/590314c04dfbff0885ebf185', json={"colors": {"red": currentValues['red'], "green": currentValues['green'], "blue": currentValues['blue'], "white": currentValues['white']}})
        except requests.exceptions.ConnectionError:
           print "connection error"

        print "update!!"

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

#encRed = Encoder(20, 21, 15, "red")
#encGreen = Encoder(17, 18, 15, "green")
#encBlue = Encoder(22, 23, 15, "blue")
#encWhite = Encoder(24, 25, 15, "white")
#
#
##enc2 = Encoder(5, 15)
#encRed.displayEncoder()
#encGreen.displayEncoder()
#encBlue.displayEncoder()
#encWhite.displayEncoder()

manual_controll = Controller()
manual_controll.addEncoder(
    Encoder(20, 21, 15, "red", "manual_controll"),
    Encoder(17, 18, 15, "green", "manual_controll"),
    Encoder(22, 23, 15, "blue", "manual_controll"),
    Encoder(24, 25, 15, "white", "manual_controll"))
manual_controll.listEncoders()

#enc2.displayEncoder()
while True:
   #I2C().sendRGBW(encRed.Counter, encGreen.Counter, encBlue.Counter, encWhite.Counter)
   sleep (1)

