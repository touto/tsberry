#!/usr/bin/env python
from time import sleep
import requests
from w1thermsensor import W1ThermSensor

#upper = 30.0
#lower = 20.0
#brightness = 255
sensors = []
session = requests.Session()

class tempController(object):

    upper = 30.0
    lower = 20.0
    brightness = 255


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


    sensor = W1ThermSensor()
    
    # get id of the area which we want to controll
    
    def calc_brightness(self, value):
            output = ((value / 100.0) * self.brightness)
            return output
    
    def update(self):
    	self.temperature_in_celsius = self.sensor.get_temperature()
    	#temperature_in_celsius = 40.0
    	if (self.temperature_in_celsius >= self.upper):
    		self.red = self.calc_brightness(255)
    		blue = 0
    	elif (self.temperature_in_celsius <= self.lower):
    		self.red = 0
    		self.blue = self.calc_brightness(255)
    	else:
    		self.red = self.calc_brightness((((self.temperature_in_celsius-self.lower) / (self.upper - self.lower)) * 255))
    		self.blue = self.calc_brightness((((self.temperature_in_celsius-self.upper) / ( -1 * (self.upper - self.lower))) * 255))
    		## Add brightness controll
    	self.colors = {'red': self.red, 'green': 0, 'blue': self.blue, 'white': 0}
    	try:
                url = 'http://127.0.0.1/api/areas/%s' % (self.id)
                
    		session.patch(url, json={"colors": {"red": self.colors['red'], "green": self.colors['green'], "blue": self.colors['blue'], "white": self.colors['white']}})
    	except requests.exceptions.ConnectionError:
    		print "connection error"
    
    	#print "red {red}, blue: {blue}".format(**colors)
    	#sleep(0.1)

sensor1 = tempController()
sensor1.title = "temperature_1"
sensors.append(sensor1)
while True:
    for sensor in sensors:
        sensor.update()

    pass
    sleep(0.5)
