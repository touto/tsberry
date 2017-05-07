#!/usr/bin/env python
from time import sleep
import requests
from w1thermsensor import W1ThermSensor

upper = 30.0
lower = 20.0
brightness = 60
session = requests.Session()


sensor = W1ThermSensor()

def calc_brightness( value ):
        output = ((value / 100.0) * brightness)
        return output

while True:
	temperature_in_celsius = sensor.get_temperature()
	#temperature_in_celsius = 40.0
	if (temperature_in_celsius >= upper):
		red = calc_brightness(255)
		blue = 0
	elif (temperature_in_celsius <= lower):
		red = 0
		blue = calc_brightness(255)
	else:
		red = calc_brightness((((temperature_in_celsius-lower) / (upper - lower)) * 255))
		blue = calc_brightness((((temperature_in_celsius-upper) / ( -1 * (upper - lower))) * 255))
		## Add brightness controll
	colors = {'red': red, 'green': 0, 'blue': blue, 'white': 0}
	try:
		session.patch('http://127.0.0.1:5000/areas/590314c04dfbff0885ebf185', json={"colors": {"red": colors['red'], "green": colors['green'], "blue": colors['blue'], "white": colors['white']}})
	except requests.exceptions.ConnectionError:
		print "connection error"

	print "red {red}, blue: {blue}".format(**colors)
	sleep(0.1)
