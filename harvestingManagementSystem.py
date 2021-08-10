import RPi.GPIO as GPIO
import time, logging
import logging.handlers
from datetime import datetime, timedelta
from harvestingStateMachine import harvestingStateMachine
from read_inputs import read_inputs

# https://www.raspberrypi.org/documentation/linux/usage/systemd.md

# setup logs
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #controller master
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) #controller collect
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP) #tank sensor
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) #charge sensor

ch1=12
ch2=16
ch3=20
ch4=21
GPIO.setup(ch1, GPIO.OUT, initial=GPIO.LOW) #
GPIO.setup(ch2, GPIO.OUT, initial=GPIO.LOW) #
GPIO.setup(ch3, GPIO.OUT, initial=GPIO.LOW) #
GPIO.setup(ch4, GPIO.OUT, initial=GPIO.LOW) #

class harvestingStateMachineManagement(object):

    def __init__(self, name):
	# start with name
        self.name = name
        self.inputState = 0
        self.prevInputState = [0,0,0,0,0]
        self.prevState = "HelloWorld"
        self.collectStartTime = datetime.now() + timedelta(minutes=1)
        self.collectWatchDog = datetime.now()
        self.dispenseWatchDog = datetime.now()

def main():
    m=harvestingStateMachineManagement("harvestControllerManager") 
    h=harvestingStateMachine("harvestController")
    while 1:
        m.inputState = read_inputs()
        print("%s, %02x, %s, %s" % (h.state, m.inputState[0],  \
            m.collectStartTime.strftime("%m/%d/%Y, %H:%M:%S"), \
            datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
	if h.is_idle():
            if m.inputState[0] & 0x08 == 0x00:
                log.debug("water state detected, go to water monitoring state")
                h.water()
            elif m.prevState != "idle":
                log.debug("collection scheduled to start <n> min after adequate charge detected") 
                m.collectStartTime = datetime.now() + timedelta(minutes=60)
            elif m.inputState[0] & 0x01 != 0x01:
                m.collectStartTime = datetime.now() + timedelta(minutes=60)
            elif datetime.now() > m.collectStartTime:
                log.debug("collect state triggered, go collect") 
                h.collect()
                m.collectWatchDog = datetime.now() + timedelta(minutes=15)
        elif h.is_watering():	
            if m.inputState[0] & 0x08 == 0x08:
                log.debug("watering stopped, go idle") 
                h.idle()
            elif m.inputState[0] & 0x05 == 0x04:
                log.debug("deficient charge detected, go to dispense state")
                h.dispense()   
                m.dispenseWatchDog = datetime.now() + timedelta(seconds=90) 
        elif h.is_dispensing():
            if m.inputState[0] & 0x08 == 0x08:
                log.debug("watering state ended, go idle")
                h.idle()
            elif m.inputState[0] & 0x01 == 0x01:
                log.debug("proper charge level detected, go idle")
                h.idle()   
            elif m.dispenseWatchDog < datetime.now():
                log.debug("dispense watchdog triggered, go idle")
                h.idle() 
        elif h.is_collecting():
            if m.inputState[0] & 0x08 == 0x00:
                log.debug("watering state triggered, go idle")
                h.idle()
            elif m.inputState[0] & 0x02 == 0x00:
	    	log.debug("tank full state detected, go idle")
                h.idle()
            elif m.inputState[0] & 0x01 == 0x00:
		log.debug("deficient charge detected, go idle")
                h.idle()
            elif m.collectWatchDog < datetime.now():
                log.debug("collect watchdog triggered, go idle")
                h.idle() 
        if m.prevInputState[0] != m.inputState[0]:
            log.debug("Input Pins; Prev,Curr: %02x,%02x" % (m.prevInputState[0], m.inputState[0]))
        m.prevInputState = m.inputState
        m.prevState = h.state

if __name__ == "__main__":
    try:
       main()
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
       print("Cleanup IO") 
       GPIO.cleanup() # cleanup all GPIO
