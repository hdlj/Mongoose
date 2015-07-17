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
import fnmatch
from MOSParser import *
from MOSFunction import *

sourceFiles=[]
directoryCFiles="App"

globalVariableInProject = {}
functionReturnTypeInProject = {}

def main(path):
    global functionReturnTypeInProject
    get_filepaths(path)
    if not os.path.exists(path+'/'+directoryCFiles):
        os.makedirs(path+'/'+directoryCFiles)
    #1 Main function
    startPointCFile(path)
    initReturnFunctionTypeWithMOSFunction(functionReturnTypeInProject)
    #2 source files
    for file in sourceFiles:
        translatePythonInC(file,path)

    print(globalVariableInProject)
    print(functionReturnTypeInProject)


def startPointCFile(path):
    dir=os.path.basename(path)

    contentStart  = "void setup();\n"
    contentStart += "void loop();\n\n\n"
    contentStart += "int main(){\n"
    contentStart += "     MOSSerialSetup();"
    contentStart += "     setup();\n"
    contentStart += "     while(1){\n"
    contentStart += "         loop();\n"
    contentStart += "      }\n"
    contentStart += "}\n"

    projectStart = open(path+"/"+directoryCFiles+"/"+dir+"_MOSMain.c", "wt")
    projectStart.write(contentStart)
    projectStart.close()



def translatePythonInC(file,path):
    global functionReturnTypeInProject
    global globalVariableInProject
    print("MOSPYTHON "+file["name"] +".py starting")
    main=open(file["path"], "r")
    sourcePython=main.read()
    content=parseMain(sourcePython,file["name"],globalVariableInProject,functionReturnTypeInProject)
    # H file
    projectH = open(path+"/"+directoryCFiles+"/"+file["name"]+".h", "wt")
    #print(content[0])
    projectH.write(content[0])
    projectH.close()

    # C file    
    projectC = open(path+"/"+directoryCFiles+"/"+file["name"]+".c", "wt")
    #print(content[1])
    projectC.write(content[1])
    projectC.close()
    main.close()
    print("MOSPYTHON "+file["name"] +".py end")

def get_filepaths(directory):
    global sourceFiles
    for root, directories, files in os.walk(directory):
        for filename in fnmatch.filter(files, '*.py'):
            if not os.path.splitext(filename)[0] == "MOSFoundation" and not os.path.splitext(filename)[0] == "MOSSimulator":
                filepath = os.path.join(root, filename)
                sourceFiles.append({"name":os.path.splitext(filename)[0], "path": filepath})

if __name__ == '__main__':
    if len(sys.argv)>1:
        main(sys.argv[1])
    else:
        print('No path specify')
    
