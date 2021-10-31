#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import logging
import logging.handlers
from pygame import mixer
from tlc import tlc5940
import sys
import random


DIR="/home/pi/halloween"

LOG_FILENAME = "/home/pi/halloween/jacky.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
        def __init__(self, logger, level):
                """Needs a logger and a logger level."""
                self.logger = logger
                self.level = level

        def write(self, message):
                # Only log if there is a message (not just a new line)
                if message.rstrip() != "":
                        self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)

leds = tlc5940(blankpin = 27,
               progpin = 22,
               latchpin = 17,
               gsclkpin = 18,
               serialpin = 23,
               clkpin = 24)


GPIO.setmode(GPIO.BCM)
GPIO_PIR = 4

#AudioFiles = 

GPIO.setup(GPIO_PIR, GPIO.IN)

#p.start(0)

Read = 0
State = 0

mixer.init()
#mixer.music.load(DIR + '/laughter_04.mp3')
mixer.music.set_volume(1.0)

try:


    logger.info("init LEDs")
    leds.initialise()
    for led in range (0,16):
        leds.set_grey(led,0)
    leds.write_grey_values()
    leds.pulse_clk()

    logger.info("Waiting for PIR")
    while GPIO.input(GPIO_PIR) != 0:
        time.sleep(0.1)
    logger.info("Ready...")

    while True:
        Read = GPIO.input(GPIO_PIR)
        if Read == 1 and State == 0:
            #print "Erkannt!"
            logger.info("Sensed something")

            voice = random.randint(0,4)
            duration = 1
            if voice == 0:
                logger.info("ghost01")
                mixer.music.load(DIR + '/audio_ghost01.mp3')
                duration = 3
            elif voice == 1:
                logger.info('grunt01')
                mixer.music.load(DIR + '/audio_grunt01.mp3')
                duration = 5
            elif voice == 2:
                logger.info('monster01')
                mixer.music.load(DIR + '/audio_monster01.mp3')
                duration =2
            elif voice == 3:
                logger.info('/scream01')
                mixer.music.load(DIR + '/audio_scream01.mp3')
                duration = 3
            elif voice == 4:
                logger.info('scream02')
                mixer.music.load(DIR + '/audio_scream02.mp3')
                duration = 5
            else:
                logger.info('else')
                mixer.music.load(DIR + '/audio_laughter01.mp3')
                duration =2
            mixer.music.play()
#			mixer.music.load('./laughter4.mp3')
            for ins in range (2000,4096,100):
                leds.write_grey_values()
                leds.pulse_clk()
                #print 'value: ', ins
                logger.debug('value', ins)
                for led in range(0,16):
                    leds.set_grey(led,ins)
                if ins > 3900:
                    t_end = time.time() + duration
                    #print t_end
                    logger.debug(t_end)
                    while time.time() < t_end:
                        leds.pulse_clk()
                   # print time.time()
                    logger.debug(time.time())
            State = 1
        elif Read == 0 and State == 1:
           # print "Bereit ..."
            logger.info("Ready again...")
            State = 0
    time.sleep(0.1)

except KeyboardInterrupt:
   # print "Ende ..."
    logger.info("Ende...")
    GPIO.cleanup()
    leds.blank(1)

#leds.blank(1)
