'''This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>'''

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
