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




''''

This file sets the development environment
5 examples will be generated with the good makefile
Also, a project template will be generated in order to start development
Applications in this environment can be written in C, C++ and Python (with the parser)

'''


import os
import sys


directoryTemplate="Project"


ExampleDict=["Example0","Example1","Example2","Example3","Example4"]


def setup(board,port):
        path=os.path.dirname(os.path.abspath(__file__))
        # project template
        if not os.path.exists(path+'/'+directoryTemplate+"_"+board):
                os.makedirs(path+'/'+directoryTemplate+"_"+board)
        # examples
        for example in ExampleDict:
            if not os.path.exists(path+'/'+example):
                os.makedirs(path+'/'+example)
    
        # copy in every folder the good makefile
        makefile(path,board,port)

        # setup examples (imported from resource folder)
        exampleSetup(path)

        # copy inside the project template the needed resources : MOSConfig and MOSInterfaceC
        includeRessources(path,board)


def includeRessources(path,board):
        # copy MOSConfig
        os.system("cp "+path+"/Resource/MOSConfig.py "+path+"/"+directoryTemplate+"_"+board+"/MOSConfig.py")
        # copy MOSInterfaceC
        os.system("cp "+path+"/Resource/MOSInterfaceC.py "+path+"/"+directoryTemplate+"_"+board+"/MOSInterfaceC.py")

def exampleSetup(path):
        # copy from resource folder the source code of each example
        for example in ExampleDict:
            os.system("cp -a "+path+"/Resource/"+example+"/. "+path+"/"+example+"/")
        
def makefile(path,board,port):
        # generate the makefile with the current path to MOSPython
        makefile  = "CURRENT_DIRECTORY    = $(shell pwd)\n\n"
        makefile += "MOSPYTHON_DIRECTORY  = "+path+"\n"
        makefile += "MOSPYTHON            = $(MOSPYTHON_DIRECTORY)/MOSPython.py\n"
        makefile += "OS 		          = $(MOSPYTHON_DIRECTORY)/OS\n"
        makefile += "PROJECT   	          = $(CURRENT_DIRECTORY)/Project\n"
        makefile += "all: MOSPython-run\n"
        makefile += "	$(MAKE) -C $(PROJECT) OS_PATH=$(OS) PROJECT=$(PROJECT) ARDUINO_PORT="+board+"\n\n"
        makefile += "MOSPython-run:\n"
        makefile += "	python3 $(MOSPYTHON) $(CURRENT_DIRECTORY)\n"
        makefile += "	cp -v $(MOSPYTHON_DIRECTORY)/Resource/Makefile  $(PROJECT)/Makefile\n\n"
        makefile += "upload: MOSPython-run\n"
        makefile += "	$(MAKE) -C $(PROJECT) OS_PATH=$(OS) upload  PROJECT=$(PROJECT) ARDUINO_PORT="+port+"\n\n"
        makefile += "upload-store-log: MOSPython-run\n"
        makefile += "	$(MAKE) -C $(PROJECT) OS_PATH=$(OS) upload-store-log PROJECT=$(PROJECT) ARDUINO_PORT="+port+"\n\n"

        # write this makefile in the project template
        project_Makefile = open(path+"/"+directoryTemplate+"_"+board+"/Makefile", "wt")
        project_Makefile.write(makefile)
        project_Makefile.close()

        # makefile for examples
        for example in ExampleDict:
            example_1_Makefile = open(path+"/"+example+"/Makefile", "wt")
            example_1_Makefile.write(makefile)
            example_1_Makefile.close()






if __name__ == '__main__':
    if len(sys.argv)>2:
        setup(sys.argv[1],sys.argv[2])
    if len(sys.argv)>1:
        # by default, the port is tty.usbmodem1421 
        setup(sys.argv[1],'/dev/tty.usbmodem1421')
    else:
        print('You have to precise at least a board and eventually an USB port')
    

