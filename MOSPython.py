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
First MOSPython configure the parser via dictionaries 
Secondly, it launches the parser on every python found in the directory
Then it will copy all .c,.h,.cpp files in the project folder
Finally, it set Mongoose parameters (which application to launch)
The resulting folder called "Project" is ready to be uploaded
'''

import os
import sys
import fnmatch
import importlib.machinery

from MOSParser import *
from HOSApi import *
from MOSApi import *

sourceFiles=[]
CFiles = []
directoryCFiles="Project"

# global variables
GVDictP = {}
# function declarations
FDDictP = {}



def main(path):
    global FDDictP
    #0 load all source file (.py,.c,.h,.cpp)
    get_filepaths(path)
    get_c_file(path)
    #1  create a project directory if it is not done
    if not os.path.exists(path+'/'+directoryCFiles):
        os.makedirs(path+'/'+directoryCFiles)
        
    #2 add hardware, mongoose public functions, public functions from other C/C++ application
    FDDInit(FDDictP,path)

    #3 add global variable from other C/C++ application
    GVDInit(GVDictP,path)

    #move C/C++ file to project folder
    for cfiles in CFiles:
        print("copying ..." +cfiles["name"])
        os.system("cp "+cfiles["path"]+" "+path+"/"+directoryCFiles+"/")

    #4  python source files
    # -> generate the header files
    for file in sourceFiles:
        translateForH(file,path)
    # -> generate the c files
    for file in sourceFiles:
        translateForC(file,path)

    #5 configuration Mongoose
    MOSConfig(path)
    



def MOSConfig(path):
    config=importlib.machinery.SourceFileLoader('MOSConfig',path+'/MOSConfig.py').load_module()
    app = "//Configuration file\n\n"
    counter = 0
    # Application 1
    if config.APPLICATIONS["app1"]["startFunction"] != "" and config.APPLICATIONS["app1"]["stackSize"] != "":
        app += "#define APP1   "+ config.APPLICATIONS["app1"]["startFunction"]+"\n"
        app += "void "+ config.APPLICATIONS["app1"]["startFunction"]+"();\n"
        app += "#define APP1_STACK   "+ config.APPLICATIONS["app1"]["stackSize"]+"\n\n"
        counter +=1
    # Application 2
    if config.APPLICATIONS["app2"]["startFunction"] != "" and config.APPLICATIONS["app2"]["stackSize"] != "":
        app += "#define APP2   "+ config.APPLICATIONS["app2"]["startFunction"]+"\n"
        app += "void "+ config.APPLICATIONS["app2"]["startFunction"]+"();\n"
        app += "#define APP2_STACK   "+ config.APPLICATIONS["app2"]["stackSize"]+"\n\n"
        counter +=1
    # Application 3 
    if config.APPLICATIONS["app3"]["startFunction"] != "" and config.APPLICATIONS["app3"]["stackSize"] != "":
        app += "#define APP3   "+ config.APPLICATIONS["app3"]["startFunction"]+"\n"
        app += "void "+ config.APPLICATIONS["app3"]["startFunction"]+"();\n"
        app += "#define APP3_STACK   "+ config.APPLICATIONS["app3"]["stackSize"]+"\n\n"
        counter +=1
    # raise an error if no application needs to be uploaded
    if counter == 0:
        raise SyntaxError("No application is ready to be launched by Mongoose. See MOSConfig.py file. Startfunction and stackSize need to be set for at least one application")
    # generate a header file for the main function (located in the OS folder)
    projectConfig = open(path+"/"+directoryCFiles+"/MOSConfig.h", "wt")
    projectConfig.write(app)
    projectConfig.close()
    




def FDDInit(L,path):
    #1 load C/C++ functions accessible by applications 
    L.update(MONGOOSE)
    L.update(HARDWARE)
    mosinterface=importlib.machinery.SourceFileLoader('MOSInterfaceC',path+'/MOSInterfaceC.py').load_module()
    L.update(mosinterface.MOSInterfaceFDD)


def GVDInit(L,path):
    # load global variables accessible by applications 
    mosinterface=importlib.machinery.SourceFileLoader('MOSInterfaceC',path+'/MOSInterfaceC.py').load_module()
    L.update(mosinterface.MOSInterfaceGVD)


def translateForC(file,path):
    global FDDictP
    global GVDictP
    # MOSInterfaceC and MOSConfig don't need to be translated
    if file["name"] == "MOSInterfaceC" or  file["name"] == "MOSConfig":
        return

    print("MOSPYTHON C "+file["name"] +".py starting")
    main=open(file["path"], "r")
    sourcePython=main.read()
    content=parseMainC(sourcePython,file["name"],GVDictP,FDDictP)

    # C file    
    projectC = open(path+"/"+directoryCFiles+"/"+file["name"]+".c", "wt")
    projectC.write(content[0])
    projectC.close()
    GVDictP = content[1]
    FDDictP = content[2]
    
    main.close()
    print("MOSPYTHON C "+file["name"] +".py end")
    

def translateForH(file,path):
    global FDDictP
    global GVDictP
    if file["name"] == "MOSInterfaceC" or  file["name"] == "MOSConfig":
        return
    print("MOSPYTHON H "+file["name"] +".py starting")
    main=open(file["path"], "r")
    sourcePython=main.read()
    content=parseMainH(sourcePython,file["name"],GVDictP,FDDictP)

    # H file    
    projectH = open(path+"/"+directoryCFiles+"/"+file["name"]+".h", "wt")
    projectH.write(content[0])
    projectH.close()
    GVDictP = content[1]
    FDDictP = content[2]
    main.close()
    print("MOSPYTHON H "+file["name"] +".py end")
    


def get_filepaths(directory):
    global sourceFiles
    for root, directories, files in os.walk(directory):
        for filename in fnmatch.filter(files, '*.py'):
            filepath = os.path.join(root, filename)
            sourceFiles.append({"name":os.path.splitext(filename)[0], "path": filepath})

def get_c_file(directory):
    global CFiles
    for root, directories, files in os.walk(directory):
        for filename in fnmatch.filter(files, '*.cpp'):
            filepath = os.path.join(root, filename)
            CFiles.append({"name":os.path.splitext(filename)[0], "path": filepath})
        for filename in fnmatch.filter(files, '*.h'):
            filepath = os.path.join(root, filename)
            CFiles.append({"name":os.path.splitext(filename)[0], "path": filepath})
        for filename in fnmatch.filter(files, '*.c'):
            filepath = os.path.join(root, filename)
            CFiles.append({"name":os.path.splitext(filename)[0], "path": filepath})

if __name__ == '__main__':
    if len(sys.argv)>1:
        main(sys.argv[1])
    else:
        print('No path specify')
    
