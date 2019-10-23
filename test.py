#!/usr/bin/python

import RPi.GPIO as GPIO
import time

from pygame import mixer


GPIO.setmode(GPIO.BCM)
GPIO_PIR = 4

GPIO.setup(GPIO_PIR, GPIO.IN)

Read = 0
State = 0


mixer.init()
mixer.music.load('./wickedlaugh.mp3')
mixer.music.set_volume(1.0)

try:
	print "Warten, bis PIR ruht ..."
	while GPIO.input(GPIO_PIR) != 0:
		time.sleep(0.1)
	print "Ready..."

	while True:
		Read = GPIO.input(GPIO_PIR)
		if Read == 1 and State == 0:
			print "Erkannt!"
#			mixer.music.load('./laughter4.mp3')
			mixer.music.play()
			State = 1
		elif Read == 0 and State == 1:
			print "Bereit ..."
			State = 0
	time.sleep(0.1)

except KeyboardInterrupt:
	print "Ende ..."
	GPIO.cleanup()

