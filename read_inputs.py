# External module imports
import RPi.GPIO as GPIO

sampleRounds=1000

in1 = 6  # master_bhye
in2 = 13 # harvest_byhve 
in3 = 19 # tanks_not_full 
in4 = 26 # charge 

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

GPIO.setup(in1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(in2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(in3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(in4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_inputs_st():
        master = harvest = tank = charge = 0
        controllerStateLow=0
        controllerStateHigh=1

        while controllerStateLow != controllerStateHigh:
             for i in range(sampleRounds):
                master  += GPIO.input(in1)
                harvest += GPIO.input(in2)
                tank += GPIO.input(in3)
                charge += GPIO.input(in4)
             controllerStateLow  = (master>sampleRounds/3)<<3   | (harvest>sampleRounds/3)<<2   | (tank>sampleRounds/3) <<1   | (charge>sampleRounds/3)
             controllerStateHigh = (master>2*sampleRounds/3)<<3 | (harvest>2*sampleRounds/3)<<2 | (tank>2*sampleRounds/3) <<1 | (charge>2*sampleRounds/3)
             print("%04x, %04x" % (controllerStateLow, controllerStateHigh))

        return controllerStateLow, master, harvest, tank, charge

def read_inputs():
	master = harvest = tank = charge = 0
	for i in range(sampleRounds):
		master  += GPIO.input(in1)
		harvest += GPIO.input(in2)
		tank += GPIO.input(in3)
		charge += GPIO.input(in4)	
	controllerState = (master>sampleRounds/2)<<3 | (harvest>sampleRounds/2)<<2 | (tank>sampleRounds/2) <<1 | (charge>sampleRounds/2)
	return controllerState, master, harvest, tank, charge

# main
def main():
	try:
    		 while 1:
			controllerState, master, harvest, tank, charge = read_inputs()	
			print("Current Controller State: %04x (%04x %04x %04x %04x)" % (controllerState, master, harvest, tank, charge))
	except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
     		GPIO.cleanup() # cleanup all GPIO

if __name__ == "__main__":
    main()
