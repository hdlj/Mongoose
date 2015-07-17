import os
import sys
import fnmatch
from MOSParser import *
from MOSFunction import *

sourceFiles=[]
directoryCFiles="src"

globalVariableInProject = {}
functionReturnTypeInProject = {}
loopFile  = " no file "
setupFile = " no file "

def main(path):
    global functionReturnTypeInProject
    get_filepaths(path)
    initReturnFunctionTypeWithMOSFunction(functionReturnTypeInProject)
    #1 source files
    for file in sourceFiles:
        getfunctionName(file,path)
    setupSimulator(path)

def setupSimulator(path):
    global setupFile
    global loopFile
    
    if loopFile==setupFile:
        contentSim    = "from "+loopFile+" import *\n"
    else:
        contentSim    = "from "+setupFile+" import *\n"

    contentSim += "setup()\n"
    contentSim += "while(True):\n"
    contentSim += "    loop()\n"

    simulator = open(path+"/MOSSimulator.py", "wt")
    simulator.write(contentSim)
    simulator.close()

def getfunctionName(file,path):
    global functionReturnTypeInProject
    global globalVariableInProject
    global setupFile
    global loopFile
    main=open(file["path"], "r")
    sourcePython=main.read()
    functionParserForSimulator(sourcePython,file["name"],globalVariableInProject,functionReturnTypeInProject)
    if "setup" in functionReturnTypeInProject and setupFile==" no file ":
        setupFile = file["name"]
    if "loop"  in functionReturnTypeInProject and loopFile==" no file ":
        loopFile  = file["name"]
    main.close()

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
    
