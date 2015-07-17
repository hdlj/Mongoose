

def initReturnFunctionTypeWithMOSFunction(L):

	#digital function
	L['MOSDigitalSetup'] = 'void'
	L['MOSDigitalOn']    = 'void'
	L['MOSDigitalOff']	 = 'void'

	# main led on arduino
	L['MOSLedOn']        = 'void'
	L['MOSLedOff']		 = 'void'
	L['MOSLedSetup']	 = 'void'

	# serial communication
	L['MOSSerialSetup']  = 'void'
	L['MOSSerialPrint']          = 'void'
