import time


#digital function
def MOSDigitalSetup(pin : int):
	print('MOSSIMULATOR : '+str(pin)+' has been initialized')

def MOSDigitalOn(pin : int):
	print('MOSSIMULATOR : '+str(pin)+' is ON')

def MOSDigitalOff(pin : int):
	print('MOSSIMULATOR :  '+str(pin)+' is OFF')



# main led on arduino
def MOSLedOn():
	print('MOSSIMULATOR : Default led is on')

def MOSLedOff():
	print('MOSSIMULATOR : Default led is off')

def MOSLedSetup():
	print('MOSSIMULATOR : Default led is initialized')


# serial communication
def MOSSerialSetup():
	print('MOSSIMULATOR : Serial port initialized')

def MOSSerialPrint(content : str):
	print(content)

def delay(millis : int):
	print("MOSSIMULATOR : sleeping for " + str(millis) + " milliseconds")
	time.sleep(millis/1000.0)
