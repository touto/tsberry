#!/usr/bin/env python

import os
from eve import Eve
from pymongo import MongoClient
import json
import requests
from bson.objectid import ObjectId
from flask import jsonify,make_response
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

   def sendRGBW(self, address, r, g, b, w):
      self.bus.write_byte(address, r)
      self.bus.write_byte(address, g)
      self.bus.write_byte(address, b)
      self.bus.write_byte(address, w)

def post_update_bulb_callback(resource, payload):
    logging.debug("bulb %s update" % (payload['_id']))
    area = db.areas.find_one({"_id": ObjectId(resource['area'])})
    update_local_bulb(payload, area)

def post_update_area_callback(resource, payload):
    bulbs = db.bulbs.find({"area": ObjectId(payload['_id'])})
    area = db.areas.find_one({"_id": ObjectId(payload['_id'])})

    for bulb in bulbs:
        update_local_bulb(bulb, area)

def update_local_bulb(bulb, area):
    # local bulb on I2C bus with address bulb['_address']
    # address is stored as string => convert to int
    address = int(bulb['address'] ,16)

    red = area['colors']['red']
    green = area['colors']['green']
    blue = area['colors']['blue']
    white = area['colors']['white']

    I2C.sendRGBW(address, red, green, blue, white)
    logging.debug("I2C Adresse: %s, red: %s, green: %s, blue: %s, white: %s" % (address, red, green, blue, white))

port = 5000
host = '0.0.0.0'

app = Eve()


if __name__ == '__main__':

    logging.basicConfig(filename='/mnt/tmpfs/api.log',level=logging.DEBUG)

    subprocess.Popen("/usr/bin/mongorestore --drop -d eve /opt/mongo_prepare/dump/eve/", shell=True)
    I2C = I2C()

    app.on_updated_areas += post_update_area_callback
    app.on_updated_bulbs += post_update_bulb_callback
    app.run(host=host, port=port)

