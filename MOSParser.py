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
This file contains the source code of the parser
It is responsible of parsing python code in order to generate c code
'''



import copy
import ast


# counter for indentation in the destination file: it makes the code more readable
numberIndentation=0


# maps python function to their equivalent in Mongoose or in C
pythonFunction={'print':'printf','delay':'MOSSleep'}

# dictionary for c type available
# change this dictionnary to have access to other kind of integer for instance
CTypes={"str":"string", "int":"uint16_t","float":"float","bool":"bool","list":"CList","loopCounter":"uint8_t"}

#dictionary for list functions
CListFunction={"store":"listSetElementAt", "load":"listElementAt","add":"listAddElement"}


# dictionary : local variable to its  type
LVDict = {}
#dictionary : global variable to its  type
GVDict = {}
#dictionary : function declaration to its return type
FDDict = {}

#global variable to store the file name. It is used when an error is raised
file=''

# current line which is parsed:
currentLine = 0


# function to go through the AST in order to create a header file which makes this source code accessible from other C/C++ and Python code
def parseMainH(sourceContent,nameFile,GVDictP,FDDictP):
    global file
    global GVDict
    global FDDict
    GVDict=GVDictP
    FDDict=FDDictP
    file=nameFile
    p=ast.parse(sourceContent)

    header  = "#ifndef " + nameFile.upper() + "_H\n"
    header += "#define " + nameFile.upper() + "_H\n\n\n"
    header += headerFileParser(p.body) + "\n"
    header += "\n\n#endif\n"
    return (header,GVDict,FDDict)

# function to go through the AST in order to translate python code to c code
def parseMainC(sourceContent,nameFile,GVDictP,FDDictP):
    global file
    global GVDict
    global FDDict
    GVDict=GVDictP
    FDDict=FDDictP
    file=nameFile
    p=ast.parse(sourceContent)
    source  = '#include "'+nameFile+'.h"\n\n'
    source += bodyParser(p.body)

    return (source,GVDict,FDDict)


# function to only parse function declaration and global variable declaration
def headerFileParser(body):
    result=[]
    for line in body:
        result.append(statement(line,True))
    separator="\n"+indentation()
    return separator.join(result)

# function to parse the body of a block code. It is used for the loops and function's body
def bodyParser(body):
    result=[]
    for line in body:
        result.append(statement(line, False))
    separator="\n"+indentation()
    return separator.join(result)

# function to translate a if loop in C
def ifLoop(l):
    global numberIndentation
    global currentLine
    if l.lineno is not None:
    #0 store current line:
        currentLine = l.lineno

    #1 get the test contained inside the if loop
    test=expr(l.test,False)
    #2 new block 
    numberIndentation=numberIndentation+1

    #3 build the final C declaration with the test and the body of the if loop
    declaration=''
    if(l.orelse):
        declaration='if('+test+'){\n'+indentation()+bodyParser(l.body)+'\n'+indentationAdjusted(-1)+'}\n'+indentationAdjusted(-1)+'else'
        numberIndentation=numberIndentation-1
        first=1
        # go through all stage of the if loop (if, elif and else) and add them to the final declaration
        for ifStmt in l.orelse:
            if isinstance(ifStmt,ast.Expr):
                if first==1:
                    numberIndentation=numberIndentation+1
                    first=0
                    declaration=declaration+'{\n'+indentation()+statement(ifStmt)
                else:
                    declaration=declaration+'\n'+indentation()+statement(ifStmt)

            else:
                declaration=declaration+' '+statement(ifStmt)
        if first==0:
            declaration=declaration+'\n'+indentationAdjusted(-1)+'}\n'
            numberIndentation=numberIndentation-1
    else:
        # case with only one stage : if ... without else and elif
        declaration='if('+test+'){\n'+indentation()+bodyParser(l.body)+'\n'+indentationAdjusted(-1)+'}'
        numberIndentation=numberIndentation-1       

    return declaration


# function to go through a while loop and its body        
def whileLoop(l):
    global numberIndentation
    global currentLine
    if l.lineno is not None:
    #0 store current line:
        currentLine = l.lineno

    test=expr(l.test,False)
    # increase the indentation temporary for the whil loop body position
    numberIndentation=numberIndentation+1
    # contrary to if loops there is only one stage:
    declaration='while('+test+'){\n'+indentation()+bodyParser(l.body)+'\n'+indentationAdjusted(-1)+'}'
    # decrease the indentation when the while loop ends
    numberIndentation=numberIndentation-1
    return declaration

# function to go through a for loop 
# multiple case: for x in range(100), for x in range(2,100) and for x in l

def forLoop(l):
    global numberIndentation
    global currentLine
    if l.lineno is not None:
    #0 store current line:
        currentLine = l.lineno

    attrs = vars(l)
    numberIndentation=numberIndentation+1
    # the two first case are considered here
    if isinstance(l.target,ast.Name) and isinstance(l.iter,ast.Call) and expr(l.iter.func,False)=='range':
        arg=[expr(arg,False) for arg in l.iter.args]
        name=expr(l.target,False)
        # case: for x in range(100)
        if(len(arg)==1):
            declaration= CTypes["loopCounter"]+' '+name+ ';\n'+indentationAdjusted(-1)+' for('+name+'=0;'+name+'<'+arg[0]+';'+name+'++){\n'+indentation()+bodyParser(l.body)+'\n'+indentationAdjusted(-1)+'}'
            numberIndentation=numberIndentation-1
            return declaration
        # case for x in range(2,100)
        elif(len(arg)==2):
            declaration= CTypes["loopCounter"]+' '+name+ ';\n'+indentationAdjusted(-1)+' for('+name+'='+arg[0]+';'+name+'<'+arg[1]+';'+name+'++){\n'+indentation()+bodyParser(l.body)+'\n'+indentationAdjusted(-1)+'}'
            numberIndentation=numberIndentation-1
            return declaration

    if isinstance(l.target,ast.Name) and isinstance(l.iter,ast.Name):
        # raise an error if the target is already a variable in the scope
        if l.target.id in GVDict.keys() or l.target.id in LVDict.keys():
            NameError(file+"| "+str(currentLine)+" : "+l.target.id+" is already declared")
        # the last case is considered here
        if l.iter.id in GVDict.keys() or l.iter.id in LVDict.keys():
            # case :for x in l
            name=expr(l.target,False)
            clist=expr(l.iter,False)
            # a counter has to be added in order to let the target be the real iterator used un the code
            # this iterator become temporary a local variable in order to avoid other declarations
            # Clist are arrays of uint16_t
            LVDict[name]=CTypes["int"]

            declaration=CTypes["loopCounter"]+' '+name+'_mos_iterator; \n'+indentationAdjusted(-1)+' for('+name+'_mos_iterator=0;'+name+'_mos_iterator++;'+name+'<'+clist+'.size){\n'+indentation()+'uint16_t '+name+' = '+clist+'.data['+name+'_mos_iterator]\n'+bodyParser(l.body)+'\n'+indentationAdjusted(-1)+'}'
            
            # we remove the etirator from the local dictionary
            if name in LVDict: del myDict[name]
            # incrementation is decreased because the block ends
            numberIndentation=numberIndentation-1
            return declaration
        else:
            # raise an error if a list is not used in this case.
            NameError(file+"| "+str(currentLine)+" : "+l.iter.id+" is not a list")
            return
    return '//NOT RECOGNIZED'
    
    
    
# function parse a function definition    
def functionDef(f, withBody):
    global LVDict
    global GVDict

    global currentLine
    if f.lineno is not None:
    #0 store current line:
        currentLine = f.lineno

    returnType = expr(f.returns,True)
    # by default the return type is void
    if len(returnType) == 0:
        returnType='void'
    else:
        returnType = returnType[1]
    #check if the functin is already declared
    if not withBody and f.name in FDDict :
        raise NameError(file+"| "+str(currentLine)+": "+f.name+" has been already declared")
    # the function is added to the function declaration dictionary    
    FDDict[f.name] = returnType
    # LVDict starts empty because local variables are specific to one function declaration
    LVDict = {}
    # The list of arguments is built with the type detection mechanism
    argumentList=[]
    for arg in f.args.args:
        typeArg     = expr(arg.annotation,True)[1]
        variableArg = arg.arg
        argumentList.append(typeArg + ' ' + variableArg)
        if variableArg in GVDict.keys():
            raise NameError(file+"| "+str(currentLine)+" : one argument of the function '"+f.name+"' is already declared as a global variable")
        # this arguments are considered as local variable avoiding other variable declaration
        LVDict[variableArg]=typeArg

    arguments=",".join(argumentList)
    # if the body does not need to be parsed, return only the C function declaration (for hearler file)
    if not withBody:
        return returnType +' '+ f.name+'('+arguments+');'


    global numberIndentation
    numberIndentation=numberIndentation+1
    # final declaration of the function
    declaration=returnType +' '+ f.name+'('+arguments+') {\n'+indentation()+bodyParser(f.body)+'\n}\n'
    numberIndentation=numberIndentation-1
    return declaration

# expression declaration, it can be also a variable declaration without initialisation
def expressionDef(node):
    global currentLine
    if node.lineno is not None:
    #0 store current line:
        currentLine = node.lineno
    return expr(node.value,False)+';'


# function to detect the type of a variable
def expr(exp, withType):
    
    # string
    if isinstance(exp,ast.Str):
        if withType:
            return ('"'+exp.s+'"',CTypes['str'])
        else:
            return '"'+exp.s+'"'
    # name : can be a function call, variable name, etc.
    if isinstance(exp,ast.Name):
        if withType:
            if  exp.id in CTypes.keys(): 
                return (exp.id,CTypes[exp.id])
            if  exp.id in LVDict:
                return (exp.id,LVDict[exp.id])
            return (exp.id, 'void *')
        else:
            return exp.id
    # list
    if isinstance(exp,ast.List):
        attrs = vars(exp)

        if withType:
            return ('',CTypes['list'])
        else:
            return ''
    # properties fo the list (access and storage)
    if isinstance(exp,ast.Subscript):
        # access to the list - ex: L[5]
        if isinstance(exp.ctx,ast.Load):
            if withType:
                return (CListFunction["load"] +'('+expr(exp.slice.value,False)+',&'+exp.value.id+')',CTypes['int'])
            else:
                return CListFunction["load"]+'('+expr(exp.slice.value,False)+',&'+exp.value.id+')'
        # set an element in the list - ex: L[5] = 3
        if isinstance(exp.ctx,ast.Store):
            if withType:
                return (exp.value.id,CTypes['int'],CListFunction["store"]+'('+expr(exp.slice.value,False)+',&'+exp.value.id)
            else:
                return (exp.value.id, CListFunction["store"]+'('+expr(exp.slice.value,False)+',&'+exp.value.id)
        if withType:
            return ('',CTypes['list'])
        else:
            return ''
    # constant names
    if isinstance(exp, ast.NameConstant):
        if withType:
            return nameConstant(exp)
        return nameConstant(exp)[0]
    # Number is for integer and float
    if isinstance(exp,ast.Num):
        if withType:
            # integer
            if isInt(str(exp.n)):
                return (str(exp.n), CTypes['int'])
            # float
            elif isfloat(str(exp.n)):
                return (str(exp.n),CTypes['float'])
        return str(exp.n)
    # a function call
    if isinstance(exp, ast.Call):
        #1
        name=expr(exp.func,False)
        if name in pythonFunction:
            name=pythonFunction[name]
        #2
        arguments=""
        for arg in exp.args:
            if  isinstance(arg,ast.Name) and  arg.id in FDDict.keys() and FDDict[arg.id] == "void":
                arguments+='&'+expr(arg,False)+','
            else:
                arguments+=expr(arg,False)+','
        arguments=arguments[:-1]
        if withType:
            return (name +'('+arguments+')', FDDict[name])
        return name+'('+arguments+')'
    # comparison between two value/svariables
    if isinstance(exp,ast.Compare):
        leftSide=expr(exp.left,False)
        op="".join([comparaisonOperator(op) for op in exp.ops])
        comparator="".join([expr(comp,False) for comp in exp.comparators])
        return leftSide+op+comparator
    # bool
    if  isinstance(exp,ast.BoolOp):
        expressions=[expr(value,False) for value in exp.values]
        return expressions[0]+boolOperator(exp.op)+expressions[1]
    # operation on booleans
    if isinstance(exp,ast.BinOp):
        leftPart=expr(exp.left,True)
        op=operator(exp.op)
        rightPart=expr(exp.right,True)
        if withType:
            return operatorInC(leftPart,op,rightPart)
        return operatorInC(leftPart,op,rightPart)[0]
    # strange cases
    if exp is None:
        return ''
    return '//NOT RECOGNIZED'
    
# type detection works with assignement
# this function goes through the node in order to get the global type in the expression
# an integer can be assigned to a float and also in the opposite
def assignDef(node,onlydeclaration):
    global currentLine
    if node.lineno is not None:
    #0 store current line:
        currentLine = node.lineno
    global LVDict
    global GVDict
    global parsingtype
    if len(node.targets)>0 :
        target = expr(node.targets[0],False)
        value  = expr(node.value,True)

        # Assignment for global variable (header file)

        if onlydeclaration:
            if not target in GVDict.keys():
                GVDict[target]=[value[1],False]
                return value[1] +' '+target+';'
            else:
                raise SyntaxError(file+"| "+str(currentLine)+": Redefinition of  '"+target+"' (global variable)")
            return ''
        # Assignment for global variable (c file)
        if target in GVDict.keys():

            if GVDict[target][0] == CTypes['list']:
                if not GVDict[target][1]:
                    GVDict[target][1]=True
                    if value[1] == CTypes['list']:
                        return value[1] +' '+target+';'
                if  value[1] != CTypes['int'] :
                    raise TypeError(file+"| "+str(currentLine)+" : Assign '"+target+"' (global variable), which contains integers  with '"+value[1]+"'")
                return target+','+value[0]+');'

            if value[1]!=GVDict[target][0]:
                raise TypeError(file+"| "+str(currentLine)+" : Assign '"+target+"' (global variable), which is a '"+GVDict[target][0]+"', with '"+value[1]+"'")
            if not GVDict[target][1] and value[1] != CTypes['list']:
                GVDict[target][1]=True
                return value[1] +' '+target+' = '+value[0]+';'
            return target+' = '+value[0]+';'
        # Assignment for local variable (c file)
        if target in LVDict.keys():
            if LVDict[target] == CTypes['float'] or LVDict[target] == CTypes['int']:
                if value[1] == CTypes['float'] or value[1] == CTypes['int']:
                    return target+' = '+value[0]+';'
            if value[1]!=LVDict[target]:
                raise TypeError(file+"| "+str(currentLine)+" : Assign '"+target+"' (local variable), which is a(n) '"+LVDict[target]+"', with a(n) '"+value[1]+"'")

            return target+' = '+value[0]+';'
        # Assigment for lists (needs additional function provide by Mongoose)
        if target[0] in LVDict.keys():
            if LVDict[target[0]] == CTypes['list']:
                if  value[1] != CTypes['int'] and value[1] != CTypes['float']:
                    raise TypeError(file+"| "+str(currentLine)+" : Assign '"+target[0]+"' (local variable), which contains integers  with '"+value[1]+"'")
                return target[1]+','+value[0]+');'
        # Now, the new variable can be added to the local variable dictionary
        LVDict[target]=value[1]
        # a list cannot be intialise with values: simple declaration
        if value[1] == CTypes['list']:
                return value[1] +' '+target+';'
        # default assignement         
        return value[1] +' '+target+' = '+value[0]+';'

    return ''
    

# function for boolean operator
def boolOperator(op):
    if isinstance(op,ast.Or):
        return '||'
    if isinstance(op,ast.And):
        return '&&'
    return '//NOT RECOGNIZED'

# function for comparison operator
def comparaisonOperator(op):

    if isinstance(op,ast.Eq):
        return '=='
    if isinstance(op,ast.NotEq):
        return '!='
    if isinstance(op,ast.Lt):
        return '<'
    if isinstance(op,ast.LtE):
        return '<='
    if isinstance(op,ast.Gt):
        return '>'
    if isinstance(op,ast.GtE):
        return '>='
    return '//NOT RECOGNIZED'

# basic mathematical comparison    
def operator(op):
    if isinstance(op,ast.Add):
        return '+'
    if isinstance(op,ast.Mult):
        return '*'
    if isinstance(op, ast.Div):
        return '/'
    if isinstance(op,ast.Pow):
        return '**'
    if isinstance(op,ast.FloorDiv):
        return '/'
    if isinstance(op, ast.Sub):
        return '-'
    if isinstance(op, ast.Mod):
        return '%'
    return '//NOT RECOGNIZED'

# declaration for an operator. Via the brackets, the operation order is preserved
def operatorInC(left, op, right):
    return ('('+left[0]+op+right[0]+')',"float")


def indentation ():
    return '   '*numberIndentation


def indentationAdjusted(number):
    return '  '*(numberIndentation+number)

# function to deals with statement : 
def statement (stmt, forHeaderFile):
    if forHeaderFile:
        # function declaration
        if isinstance(stmt,ast.FunctionDef):
            return functionDef(stmt,False)
        #import
        elif isinstance(stmt,ast.ImportFrom):
            return importInC(stmt.module)
        #import
        elif isinstance(stmt,ast.Import):
            return "\n".join([importInC(alias.name) for alias in stmt.names])
        #assignment
        elif isinstance(stmt,ast.Assign):
            declaration= assignDef(stmt,True)
            # global variable declaration (accessible by any other C/C++ code)
            if declaration!='':
                return 'extern '+declaration
            else:
                return ''
        else:
            return ''
    # function declaraion for c files        
    elif isinstance(stmt,ast.FunctionDef):
        return '\n\n'+functionDef(stmt,True)
    # expression declaration
    elif isinstance(stmt,ast.Expr):
        return expressionDef(stmt)
    # assignment
    elif isinstance(stmt,ast.Assign):
        return assignDef(stmt,False)
    #while
    elif isinstance(stmt,ast.While):
        return whileLoop(stmt)
    #for loop
    elif isinstance(stmt,ast.For):
        return forLoop(stmt)
    #if loop 
    elif isinstance(stmt,ast.If):
        return ifLoop(stmt)
    # c keyword
    elif isinstance(stmt,ast.Break):
        return 'break;'
    # c keyword
    elif isinstance(stmt,ast.Continue):
        return 'continue;'
    # return statement 
    elif isinstance(stmt,ast.Return):
        return 'return '+expr(stmt.value,False)+';'
    return ''

# importation declaration
def importInC(name):
    return '#include <'+name+'.h>' 

# check if a number is an integer
def isInt(value):
    try: 
        int(value)
        return True
    except ValueError:
        return False
# same for float
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def nameConstant(exp):
    if exp.value==True:
        return ('true','bool')
    elif exp.value==False:
        return ('false','bool')
    return ('//NOT RECOGNIZED','NONE')


