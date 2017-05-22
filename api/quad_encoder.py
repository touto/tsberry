#!/usr/bin/env python

import RPi.GPIO as GPIO
import threading
from time import sleep
import datetime
import requests
import json

session = requests.Session()

class Encoder(object):
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
      self.controller = controller
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
      print "Pin A : ", self.pin_a,  ", Pin B: ", self.pin_b, ", Debounce: ", self.debounce, "momi: ", self.title

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
                self.controller.update("manual_controll")
                pass
            except requests.exceptions.ConnectionError:
               print "connection error"
            #print "%s: %s" % (self.displayName(), self.Counter)
            self.Tmp = 0

      elif self.Tmp < -2:
            self.Counter -= 1
            self.mapNumber(self.Counter)
            try:
               self.controller.update("manual_controll")
            except requests.exceptions.ConnectionError:
               print "connection error"

            #print "%s: %s" % (self.displayName(), self.Counter)
            self.Tmp = 0

class Controller(object):

    encoders = []

    def __init__(self):
        self._title = None
        self._id = None
        #area= db.area.find({"title": self.title)})

    @property
    def id(self):
        #print 'called getter'
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        url = 'http://127.0.0.1/api/areas?where={"title": "%s"}' % (self.title) 
        area = session.get(url, headers={'Content-Type': 'application/json'}).json()
        if not area['_items'][0]['_id']:
            # TODO create area via api
            pass

        self.id = area['_items'][0]['_id']

    @title.deleter
    def title(self):
        del self._title


    def addEncoder(self, *encoders):
        if not self.title:
            raise ValueError('can not add encoder on controller instance without name... set controller name first!')
        for encoder in encoders:
            self.encoders.append(
                Encoder(
                    encoder['pinA'],
                    encoder['pinB'],
                    encoder['debounce'],
                    encoder['name'],
                    self
                )
            )

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
        try:
            url = 'http://127.0.0.1/api/areas/%s' % (self.id)
            session.patch(url, json={"colors": {"red": currentValues['red'], "green": currentValues['green'], "blue": currentValues['blue'], "white": currentValues['white']}})
        except requests.exceptions.ConnectionError:
           print "connection error"

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
manual_controll.title = "manual_1"
manual_controll.addEncoder(
    dict([('pinA', 20), ('pinB', 21), ('debounce', 15), ('name', 'red')]),
    dict([('pinA', 17), ('pinB', 18), ('debounce', 15), ('name', 'green')]),
    dict([('pinA', 22), ('pinB', 23), ('debounce', 15), ('name', 'blue')]),
    dict([('pinA', 24), ('pinB', 25), ('debounce', 15), ('name', 'white')])
)
#manual_controll.listEncoders()

#enc2.displayEncoder()
while True:
   #I2C().sendRGBW(encRed.Counter, encGreen.Counter, encBlue.Counter, encWhite.Counter)
   sleep (1)

