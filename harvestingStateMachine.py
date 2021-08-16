from transitions import Machine
import RPi.GPIO as GPIO
from input_masks import is_watering, is_collecting, is_full, is_charged
import random, time

# Pin Definitons:
ch1 = 12 # master_valve
ch2 = 16 # harvest_valve
ch3 = 20 # drain_valve
ch4 = 21 # 

# Pin Setup:
#GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
#GPIO.setup(ch1, GPIO.OUT) # 
#GPIO.setup(ch2, GPIO.OUT) # 
#GPIO.setup(ch3, GPIO.OUT) # 
#GPIO.setup(ch4, GPIO.OUT) # 

class harvestingStateMachine(object):

    # Define some states. 
    states = ['idle', 'watering', 'collecting', 'dispensing', 'collectingSch', 'charging']
   
    # Pin Definitons:
    ch1 = 12 # master_valve
    ch2 = 16 # harvest_valve
    ch3 = 20 # drain_valve
    ch4 = 21 # 


    def __init__(self, name):

        # start with name
        self.name = name

        # What have we accomplished today?
        self.collecting_count = 0
        self.watering_count = 0
        self.dispensing_count = 0

        #inout pins
        self.ins = 0

        # Initialize the state machine
        self.machine = Machine(model=self, states=harvestingStateMachine.states, initial='idle')

	# Initialize the state machine
        self.machine.add_transition('idle', '*', 'idle', before=['collectingOff', 'dispensingOff'])

        # The controller will turn on
        self.machine.add_transition(trigger='water', source='*', dest='watering', before=['collectingOff', 'dispensingOff', 'wateringOn'])

        # The controller will also collect on its own
        self.machine.add_transition(trigger='collect', source='*', dest='collecting', before=['collectingOff', 'dispensingOff'])
        
        # We want to dispense water too
        self.machine.add_transition('dispense', 'watering', 'dispensing', before='dispensingOn')

	# Time to reclaim some water
        self.machine.add_transition('collectSch', 'idle',  'collectingSch', before='collectingOn')

	# Time to charge
        self.machine.add_transition('charge', ['idle', 'watering', 'collecting', 'collectingSch', 'dispensing'], 'charging', before=['collectingOff','dispensingOff'])

    def wateringOn(self):
        self.watering_count += 1

    def collectingOn(self):
        if not is_full(self.ins[0]):
            self.collecting_count += 1
            print("before=collectingOn")
            GPIO.output(ch1, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(ch2, GPIO.HIGH)
        else:
            print("tank full, skipping it")

    def collectingOff(self):
        GPIO.output(ch2, GPIO.LOW)
        time.sleep(2)
        GPIO.output(ch1, GPIO.LOW)

    def dispensingOn(self):
        self.dispensing_count += 1
        print("before=dispensingOn")
        GPIO.output(ch3, GPIO.HIGH)

    def dispensingOff(self):
        print("after=dispensingOff")
        GPIO.output(ch3, GPIO.LOW)

    def read_inputs(self, ins):
        self.ins = ins

