import RPi.GPIO as GPIO
import time, logging
import logging.handlers
from datetime import datetime, timedelta
from harvestingStateMachine import harvestingStateMachine
from read_inputs import read_inputs
from input_masks import is_watering, is_collecting, is_full, is_charged 

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
        self.collectStartTime = datetime.now() + timedelta(minutes=90)

def main():
    m=harvestingStateMachineManagement("harvestControllerManager") 
    h=harvestingStateMachine("harvestController")
    while 1:
        m.inputState = read_inputs()
        h.read_inputs(m.inputState) 
        print("%s, %02x, %s, %s" % (h.state, m.inputState[0],  \
            m.collectStartTime.strftime("%m/%d/%Y, %H:%M:%S"), \
            datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
	if h.is_idle():
            if is_watering(m.inputState[0]):
                log.debug("water state detected, go to water monitoring state")
                h.water()
            elif is_collecting(m.inputState[0]):
                log.debug("manual collection state detected, go to manual collection state")
                h.collect()
            elif m.collectStartTime < datetime.now():
                m.collectStartTime = datetime.now() + timedelta(minutes=90)
                log.debug("collect state triggered, go collect") 
                h.collectSch()
        elif h.is_charging():
            if is_charged(m.inputState[0]):
                h.idle()
                m.collectStartTime = datetime.now() + timedelta(minutes=90)
                log.debug("charge looks good")
	    else:
                m.collectStartTime = datetime.now() + timedelta(minutes=90)
                if m.prevState != "charging":
                    log.debug("deficient charge, pushing start time out")
        elif h.is_watering():	
            if is_collecting(m.inputState[0]):
                log.debug("collecting state detected, go collect") 
                h.collect()
            elif not is_watering(m.inputState[0]):
                log.debug("watering stopped, go charge") 
                h.charge()
            elif not is_charged(m.inputState[0]):
                log.debug("deficient charge detected, go to dispense state")
                h.dispense()   
        elif h.is_collecting():	
            if not is_collecting(m.inputState[0]):
                log.debug("collecting state stopped, go charge") 
                h.charge()
            elif is_watering(m.inputState[0]):
                log.debug("watering started, go water") 
                h.water()
        elif h.is_dispensing():
            if not is_watering(m.inputState[0]):
                log.debug("watering stopped, go charge") 
                h.charge()
            elif is_collecting(m.inputState[0]):
                log.debug("collecting state detected, go collect") 
                h.collect()
            elif is_charged(m.inputState[0]):
                log.debug("proper charge level detected, go water")
                h.water()   
        elif h.is_collectingSch():
            if is_collecting(m.inputState[0]):
                log.debug("manual collect state detected, go collect") 
                h.collect()
            elif is_watering(m.inputState[0]):
                log.debug("watering started, go water")
                h.water()
            elif not is_charged(m.inputState[0]):
                log.debug("deficient charge, go charge")
                h.charge()
            elif is_full(m.inputState[0]):
	    	log.debug("tank full state detected, go charge")
                h.charge()
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
