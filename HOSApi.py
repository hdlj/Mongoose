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



#
# HOSApi.py
# Declare here driver functions which can be
# called by applications
# It maps function name to their return type
# Only float, bool, uint8 t , uint16 t , string and CList
# can be used
#


HARDWARE = {}
# Digital functions
HARDWARE["HOSDigitalSetup"]   =   "void"
HARDWARE["HOSDigitalOn"]	  =   "void"
HARDWARE["HOSDigitalOff"] 	  =   "void"
HARDWARE["HOSDigitalListen"]  =   "void" 

# Analog functions
HARDWARE["HOSAnalogSetup"]      =   "void" 
HARDWARE["HOSAnalogRead"]       =   "uint16_t"

# LED on port 13
HARDWARE["HOSLedOn"]   			=   "void"
HARDWARE["HOSLedOff"]	  		=   "void"
HARDWARE["HOSLedSetup"] 	    =   "void"

# Serial
HARDWARE["HOSSafePrint"]   		 =   "void"
HARDWARE["HOSSafePrintInt"]	  	 =   "void"
HARDWARE["printf"]	  		     =   "void"


#...