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



import os
import sys


directoryTemplate="BlinkLed"
def setup(board,port):
	path=os.path.dirname(os.path.abspath(__file__))
	if not os.path.exists(path+'/'+directoryTemplate+"_"+board):
		os.makedirs(path+'/'+directoryTemplate+"_"+board)
	examplePython(path,board)
	makefile(path,board,port)
	includeRessources(path,board)


def includeRessources(path,board):
	os.system("cp "+path+"/Resource/MOSFoundation.py "+path+"/"+directoryTemplate+"_"+board+"/MOSFoundation.py")

def examplePython(path,board):

	contentStart  = "from MOSFoundation import *\n\n"
	contentStart += "def setup():\n"
        contentStart += "    MOSLedSetup()\n\n"
        contentStart += "def loop():\n"
        contentStart += "    MOSLedOn()\n"
        contentStart += "    print('default led is on')\n"
        contentStart += "    delay(1000)\n"
        contentStart += "    MOSLedOff()\n"
        contentStart += "    print('default led is off')\n"
        contentStart += "    delay(1000)\n"
        contentStart += "\n"

        projectStart = open(path+"/"+directoryTemplate+"_"+board+"/blinkLed.py", "wt")
        projectStart.write(contentStart)
        projectStart.close()

def makefile(path,board,port):
	makefile = "CURRENT_DIRECTORY    = $(shell pwd)\n\n"

	makefile += "MOSPYTHON_DIRECTORY  = "+path+"\n"
	makefile += "MOSPYTHON            = $(MOSPYTHON_DIRECTORY)/MOSPython.py\n"
	makefile += "MOSSIMULATOR         = $(MOSPYTHON_DIRECTORY)/MOSSimulatorSetup.py\n"
	makefile += "MOSLib				 = $(MOSPYTHON_DIRECTORY)/lib\n"
	makefile += "ARDUINO_PROJECT   	 = $(CURRENT_DIRECTORY)/src\n"

	makefile += "all: MOSPython-run\n"
	makefile += "	$(MAKE) -C $(ARDUINO_PROJECT) MOSLib=$(MOSLib) ARDUINO_PORT="+board+"\n\n"

	makefile += "MOSPython-run:\n"
	makefile += "	python3 $(MOSPYTHON) $(CURRENT_DIRECTORY)\n"
	makefile += "	cp -v $(MOSPYTHON_DIRECTORY)/Resource/Makefile  $(ARDUINO_PROJECT)/Makefile\n\n"

	makefile += "MOSSimulator-setup:\n"
	makefile += "	python3 $(MOSSIMULATOR) $(CURRENT_DIRECTORY)\n"

	makefile += "MOSSimulator-run:\n"
	makefile += "	python3 $(CURRENT_DIRECTORY)/MOSSimulator.py\n"

	makefile += "upload: MOSPython-run\n"
	makefile += "	$(MAKE) -C $(ARDUINO_PROJECT) MOSLib=$(MOSLib) upload ARDUINO_PORT="+port+"\n\n"

	makefile += "upload-store-log: MOSPython-run\n"
	makefile += "	$(MAKE) -C $(ARDUINO_PROJECT) MOSLib=$(MOSLib) upload-store-log ARDUINO_PORT="+port+"\n\n"


	projectMakefile = open(path+"/"+directoryTemplate+"_"+board+"/Makefile", "wt")
	projectMakefile.write(makefile)
	projectMakefile.close()

if __name__ == '__main__':
    if len(sys.argv)>2:
        setup(sys.argv[1],sys.argv[2])
    if len(sys.argv)>1:
        setup(sys.argv[1],'/dev/tty.usbmodem1421')
    else:
        print('You have to precise at least a board and eventually an USB port')
    

