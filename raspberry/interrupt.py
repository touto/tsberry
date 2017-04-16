#!/usr/bin/env python
import RPi.GPIO as GPIO
import threading
from time import sleep
import datetime

                  # GPIO Ports
Enc_A = 4              # Encoder input A: input GPIO 4
Enc_B = 14                   # Encoder input B: input GPIO 14
Counter = 0
Tmp = 0

Rotary_counter = 0           # Start counting from 0
Current_A = 1               # Assume that rotary switch is not
Current_B = 1               # moving while we init software

last_tick = datetime.datetime.now()

LockRotary = threading.Lock()      # create lock for rotary switch
   

# initialize interrupt handlers
def init():
   GPIO.setwarnings(True)
   GPIO.setmode(GPIO.BCM)               # Use BCM mode
                                 # define the Encoder switch inputs
   GPIO.setup(Enc_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)             
   GPIO.setup(Enc_B, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)

   GPIO.add_event_detect(Enc_A, GPIO.BOTH, callback=interrupt_both)
   GPIO.add_event_detect(Enc_B, GPIO.BOTH, callback=interrupt_both)

   return

def interrupt_both(arg):
   global Counter
   global Tmp
   global last_tick
   divider = float(10000)

   current_tick = datetime.datetime.now()

   tick = current_tick - last_tick

   multiplier = (1 / float (tick.microseconds / divider))
   #print "\n"
   #if tick.microseconds < 8853:
   #   print "fast"
   #else:
   #   print "slow"

   if arg == Enc_A:

      a = datetime.datetime.now()

      if GPIO.input(Enc_A)^GPIO.input(Enc_B):
         Tmp += 1
      else:
         Tmp -= 1

   elif arg == Enc_B:

      if GPIO.input(Enc_A)^GPIO.input(Enc_B):
         Tmp -= 1
      else:
         Tmp += 1

   if multiplier < 1:
      multiplier = 1
   #print "___________\n"
   #print int(multiplier)
   #print "___________\n"
   #print int((Tmp)/4)
   last_tick = datetime.datetime.now()

   if Tmp > 2:
         Counter += 1
         print Counter
         Tmp = 0

   elif Tmp < -2:
         Counter -= 1
         print Counter
         Tmp = 0


def interrupt_A(arg):
   global Counter
   if GPIO.input(Enc_B) == 0:
      Counter += 1
      print Counter
   else:
      return

def interrupt_B(arg):
   global Counter
   if GPIO.input(Enc_A) == 0:
      Counter -= 1
      print Counter
   else:
      return


# Rotarty encoder interrupt:
# this one is called for both inputs from rotary switch (A and B)
def rotary_interrupt(A_or_B):
   #print "interrupt"
   print A_or_B
   #print GPIO.input(Enc_A)^GPIO.input(Enc_B)
   #print GPIO.input(Enc_A)
   #print GPIO.input(Enc_B)
   return                                 # THAT'S IT

# Main loop. Demonstrate reading, direction and speed of turning left/rignt
def main():

   init()                              # Init interrupts, GPIO, ...
            
   while True :                        # start test
      sleep(0.1)                        # sleep 100 msec
      
# start main demo function
main()
