#!/usr/bin/env python
brightness = 50
#x=100.0

def calc_brightness( value ):
        output = ((value / 100.0) * brightness)
        return output
#
print calc_brightness(100)
