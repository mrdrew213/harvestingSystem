from transitions import Machine
import RPi.GPIO as GPIO
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
    states = ['idle', 'watering', 'dispensing', 'collecting']
   
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

        # Initialize the state machine
        self.machine = Machine(model=self, states=harvestingStateMachine.states, initial='idle')

        # The controller will turn on
        self.machine.add_transition(trigger='water', source=['idle','dispensing'], dest='watering', before='wateringOn')

        # We want to dispense water too
        self.machine.add_transition('dispense', 'watering', 'dispensing', before='dispensingOn')
        
	# Time to reclaim some water
        self.machine.add_transition('collect', 'idle', 'collecting', before='collectingOn')

	# Initialize the state machine
        self.machine.add_transition('idle', '*', 'idle', before=['collectingOff', 'dispensingOff'])

    def wateringOn(self):
        self.watering_count += 1

    def collectingOn(self):
        self.collecting_count += 1
        print("before=collectingOn")
        GPIO.output(ch1, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(ch2, GPIO.HIGH)

    def collectingOff(self):
        print("after=collectingOff")
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

