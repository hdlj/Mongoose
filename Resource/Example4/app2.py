#=============================================================================
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>'''
#
#    Date: 2015
#
#===============================================================================






import MOSFoundation
def app2(): 
	HOSAnalogSetup()
	HOSDigitalSetup(3) 
	HOSDigitalListen(2,buttonListener) 
	while(True):
		MOSSleep (1000)
		result = HOSAnalogRead(0)
		MOSSleep (1000)

def buttonListener():
	for x in range (4):
		HOSDigitalOn(3) 
		MOSSleep(500) 
		HOSDigitalOff(3)
		MOSSleep (500)
