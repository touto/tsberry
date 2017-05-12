#!/usr/bin/env python

import os
from eve import Eve
from pymongo import MongoClient
import json
#from pprint import pprint
import requests
#import flask
#from bson.json_util import dumps
#from bson import Binary, Code
#from bson.json_util import dumps
#import bson
from bson.objectid import ObjectId
from flask import jsonify,make_response
#from flask import jsonify

import threading
from time import sleep
import datetime
import smbus
import subprocess
import logging


client = MongoClient()
db = client.eve

class I2C:
   'I2C com class'
   bus = smbus.SMBus(1)
   def writeNumber(self, value):
      bus.write_byte(address, value)
      #print "write"
      # bus.write_byte_data(address, 0, value)
      return -1

   def readNumber(self):
      number = bus.read_byte(address)
      # number = bus.read_byte_data(address, 1)
      return number

   def sendRGBW(self, address, r, g, b, w):
      self.bus.write_byte(address, r)
      self.bus.write_byte(address, g)
      self.bus.write_byte(address, b)
      self.bus.write_byte(address, w)
      #print "_____"
      #print r
      #print g
      #print b
      #print w
      #print "____"

def post_get_callback(resource, request, payload):
    print 'A GET on the "%s" endpoint was just performed!' % resource
    #print payload['_id']

def post_update_callback(resource, payload):
    bulbs = db.bulbs.find({"area": ObjectId(payload['_id'])})
    for bulb in bulbs:
        #print bulb
        if bulb['remote']:
            # TODO
            print "bulb is remote"
        else:
            # local bulb on I2C bus with address bulb['_address']
            # address is stored as string => convert to int
            address = int(bulb['address'] ,16)

            try:
                red = resource['colors']['red']
            except KeyError:
                # color was not sent in request => use last value
                red = payload['colors']['red']

            try:
                green = resource['colors']['green']
            except KeyError:
                # color was not sent in request => use last value
                green = payload['colors']['green']

            try:
                blue = resource['colors']['blue']
            except KeyError:
                # color was not sent in request => use last value
                blue = payload['colors']['blue']

            try:
                white = resource['colors']['white']
            except KeyError:
                # color was not sent in request => use last value
                white = payload['colors']['white']

            I2C.sendRGBW(address, red, green, blue, white)
            logging.debug("I2C Adresse: %s, red: %s, green: %s, blue: %s, white: %s" % (address, red, green, blue, white))

        #print bulb['address']
    #print resource['colors']['red']
    #print resource['colors']['green']
    #print resource['colors']['blue']
    #print resource['colors']['white']

    #print resource["area"]
    #print type(resource)
    #print resource.json
    #print payload.json

# Heroku support: bind to PORT if defined, otherwise default to 5000.
if 'PORT' in os.environ:
    port = int(os.environ.get('PORT'))
    # use '0.0.0.0' to ensure your REST API is reachable from all your
    # network (and not only your computer).
    host = '0.0.0.0'
else:
    port = 5000
    host = '0.0.0.0'

app = Eve()


if __name__ == '__main__':
    #app.on_post_GET += post_get_callback
    #app.on_post_PATCH_areas += post_patch_area_callback
    logging.basicConfig(filename='/mnt/tmpfs/api.log',level=logging.DEBUG)

    subprocess.Popen("/usr/bin/mongorestore --drop -d eve /opt/mongo_prepare/dump/eve/", shell=True)
    sleep(1)
    bulbs = db.bulbs.find()
    for bulb in bulbs:
        #print "yoloyoloyoloyoloyoloyolo"
        #print "create new connection to bulb"
        #print bulb
        I2C = I2C()
    app.on_updated_areas += post_update_callback
    app.run(host=host, port=port)

