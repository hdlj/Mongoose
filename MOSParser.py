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

import copy
import ast
from MOSHardware import *

numberIndentation=0

CTypes={"str":"string", "int":"int16_t","float":"float","bool":"bool"}
CoreModule = ["MOSFoundation"]

localVariable = {}
globalVariable = {}
functionReturnType = {}
file=''

def parseMain(sourceContent,nameFile,globalVariableInProject,functionReturnTypeInProject):
    global file
    global globalVariable
    global functionReturnType
    globalVariable=globalVariableInProject
    functionReturnType=functionReturnTypeInProject
    file=nameFile
    p=ast.parse(sourceContent)

    #1
    header  = "#ifndef " + nameFile.upper() + "_H\n"
    header += "#define " + nameFile.upper() + "_H\n\n\n"
    header += headerFileParser(p.body) + "\n"
    header += "\n\n#endif\n"

    #2
    source  = '#include "'+nameFile+'.h"\n\n'
    source += bodyParser(p.body)

    return (header,source)

def functionParserForSimulator(sourceContent,nameFile,globalVariableInProject,functionReturnTypeInProject):
    global file
    global globalVariable
    global functionReturnType
    globalVariable=globalVariableInProject
    functionReturnType=functionReturnTypeInProject
    file=nameFile
    p=ast.parse(sourceContent)
    headerFileParser(p.body)

def headerFileParser(body):
    result=[]
    for line in body:
        result.append(statement(line,True))
    separator="\n"+indentation()
    return separator.join(result)


def bodyParser(body):
    result=[]
    for line in body:
        result.append(statement(line, False))
    separator="\n"+indentation()
    return separator.join(result)


def ifLoop(l):
    global numberIndentation
    test=expr(l.test,False)
    numberIndentation=numberIndentation+1
    declaration=''
    if(l.orelse):
        declaration='if('+test+'){\n'+indentation()+bodyParser(l.body)+'\n'+indentationAdjusted(-1)+'}\n'+indentationAdjusted(-1)+'else'
        numberIndentation=numberIndentation-1
        first=1
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
        declaration='if('+test+'){\n'+indentation()+bodyParser(l.body)+'\n'+indentationAdjusted(-1)+'}'
        numberIndentation=numberIndentation-1       

    return declaration
        
def whileLoop(l):
    global numberIndentation
    test=expr(l.test,False)
    numberIndentation=numberIndentation+1
    declaration='while('+test+'){\n'+indentation()+bodyParser(l.body)+'\n'+indentationAdjusted(-1)+'}'
    numberIndentation=numberIndentation-1
    return declaration
    
def forLoop(l):
    global numberIndentation
    numberIndentation=numberIndentation+1
    if isinstance(l.target,ast.Name) and isinstance(l.iter,ast.Call) and expr(l.iter.func,False)=='range':
        arg=[expr(arg,False) for arg in l.iter.args]
        name=expr(l.target,False)
        if(len(arg)==1):
            declaration='for(int '+name+'=0;'+name+'++;'+name+'<'+arg[0]+'){\n'+indentation()+bodyParser(l.body)+'\n'+indentationAdjusted(-1)+'}'
            numberIndentation=numberIndentation-1
            return declaration
        elif(len(arg)==2):
            declaration='for(int '+name+'='+arg[0]+';'+name+'++;'+name+'<'+arg[1]+'){\n'+indentation()+bodyParser(l.body)+'\n'+indentationAdjusted(-1)+'}'
            numberIndentation=numberIndentation-1
            return declaration
    return '//NOT RECOGNIZED'
    
    
    
    
def functionDef(f, withBody):
    global localVariable
    global globalVariable
    global isParserInFunctionBody
    returnType = expr(f.returns,True)
    if len(returnType) == 0:
        returnType='void'
    else:
        returnType=returnType[1]
    functionReturnType[f.name]=returnType
    localVariable={}
    argumentList=[]
    for arg in f.args.args:
        typeArg     = expr(arg.annotation,True)[1]
        variableArg = arg.arg
        argumentList.append(typeArg + ' ' + variableArg)
        if variableArg in globalVariable.keys():
            raise NameError(file+" : one argument of the function '"+f.name+"' is already declared as a global variable")
        localVariable[variableArg]=typeArg

    arguments=",".join(argumentList)
    if not withBody:
        return returnType +' '+ f.name+'('+arguments+');'


    global numberIndentation
    numberIndentation=numberIndentation+1
    declaration=returnType +' '+ f.name+'('+arguments+') {\n'+indentation()+bodyParser(f.body)+'\n}\n'
    numberIndentation=numberIndentation-1
    return declaration

def expressionDef(node):
    if isinstance(node.value,ast.Name):
        print('simple variable')
    return expr(node.value,False)+';'

def expr(exp, withType):
    print(exp)
   # if isinstance(exp,ast.arg):
#        if exp.annotation is None:
#            return 'void *'+exp.arg
#        else:
#            return exp.annotation.id + ' '+exp.arg
    if isinstance(exp,ast.Str):
        if withType:
            return ('"'+exp.s+'"',CTypes['str'])
        else:
            return '"'+exp.s+'"'
    if isinstance(exp,ast.Name):
        if withType:
            if  exp.id in CTypes.keys(): 
                return (exp.id,CTypes[exp.id])
            if  exp.id in localVariable:
                return (exp.id,localVariable[exp.id])
            return (exp.id, 'void *')
        else:
            return exp.id
    if isinstance(exp,ast.List):
        return '// List NOT RECOGNIZED YET'
    if isinstance(exp, ast.NameConstant):
        if withType:
            return nameConstant(exp)
        return nameConstant(exp)[0]
    if isinstance(exp,ast.Num):
        if withType:
            if isInt(str(exp.n)):
                return (str(exp.n), CTypes['int'])
            elif isfloat(str(exp.n)):
                return (str(exp.n),CTypes['float'])
        return str(exp.n)
    if isinstance(exp, ast.Call):
        #1
        name=expr(exp.func,False)
        if name in hardwareFunction:
            name=hardwareFunction[name]
        #2
        print(name)
        for arg in exp.args:
            print(arg)

        arguments=",".join([expr(arg,False) for arg in exp.args])
        if withType:
            return (name +'('+arguments+')', functionReturnType[name])
        return name+'('+arguments+')'
    if isinstance(exp,ast.Compare):
        leftSide=expr(exp.left,False)
        op="".join([comparaisonOperator(op) for op in exp.ops])
        comparator="".join([expr(comp,False) for comp in exp.comparators])
        return leftSide+op+comparator
    if  isinstance(exp,ast.BoolOp):
        expressions=[expr(value,False) for value in exp.values]
        return expressions[0]+boolOperator(exp.op)+expressions[1]
    if isinstance(exp,ast.BinOp):
        leftPart=expr(exp.left,True)
        op=operator(exp.op)
        rightPart=expr(exp.right,True)
        if withType:
            return operatorInC(leftPart,op,rightPart)
        return operatorInC(leftPart,op,rightPart)[0]
    if exp is None:
        return ''
    print(exp)
    return '//NOT RECOGNIZED'
    

def assignDef(node,onlydeclaration):
    #print(node.value)
    #target=",".join([expr(tar,False) for tar in node.targets])
    global localVariable
    global globalVariable
    if len(node.targets)>0 :
        target = expr(node.targets[0],False)
        value  = expr(node.value,True)

        if onlydeclaration:
            if not target in globalVariable.keys():
                globalVariable[target]=[value[1],False]
                return value[1] +' '+target+';'
            else:
                raise SyntaxError(file+" : Redefinition of  '"+target+"' (global variable)")
            return ''

        if target in globalVariable.keys():
            if value[1]!=globalVariable[target][0]:
                raise TypeError(file+" : Assign '"+target+"' (global variable), which is a '"+globalVariable[target][0]+"', with '"+value[1]+"'")
            if not globalVariable[target][1]:
                globalVariable[target][1]=True
                return value[1] +' '+target+' = '+value[0]+';'
            return target+' = '+value[0]+';'

        if target in localVariable.keys():
            if value[1]!=localVariable[target]:
                raise TypeError(file+" : Assign '"+target+"' (local variable), which is a(n) '"+globalVariable[target][0]+"', with a(n) '"+value[1]+"'")
            return target+' = '+value[0]+';'
        localVariable[target]=value[1]
        return value[1] +' '+target+' = '+value[0]+';'

    return ''
    





def getFunctionBlock(sourceCodeArray):
    result=[]
    currentBlock=[]
    indentation=0
    for nextline in sourceCodeArray:
        line=nextline.rstrip('\n')
        if(len(line.lstrip())==0):
            continue           
        elif('def ' in line):
            if(currentBlock!=[]):
                result=result+[currentBlock]
            currentBlock=[line]
            indentation=0
        elif(len(currentBlock)==1):
            indentation=len(line) - len(line.lstrip())
            if(indentation>0):
                currentBlock=currentBlock+[line]
            else:
                result=result+[currentBlock]
                currentBlock=[]
        elif(len(currentBlock)>1):
            if(len(line) - len(line.lstrip())>=indentation):
                currentBlock=currentBlock+[line]
            else:
                result=result+[currentBlock]
                currentBlock=[]
    if(currentBlock!=[]):
        result=result+[currentBlock]
    print(result)
    return

def getNameFunction():
    print(name)


def boolOperator(op):
    if isinstance(op,ast.Or):
        return '||'
    if isinstance(op,ast.And):
        return '&&'
    return '//NOT RECOGNIZED'

    
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


def operatorInC(left, op, right):
    if op=='+':
        if left[1]=='string' and right[1]=='string':
            return ('MOSStringConcatenate('+left[0]+','+right[0]+')','string')
    return ('('+left[0]+op+right[0]+')',left[1])


def indentation ():
    return '   '*numberIndentation


def indentationAdjusted(number):
    return '  '*(numberIndentation+number)


def statement (stmt, forHeaderFile):
    if forHeaderFile:
        if isinstance(stmt,ast.FunctionDef):
            return functionDef(stmt,False)
        elif isinstance(stmt,ast.ImportFrom):
            return importInC(stmt.module)
        elif isinstance(stmt,ast.Import):
            return "\n".join([importInC(alias.name) for alias in stmt.names])
        elif isinstance(stmt,ast.Assign):
            declaration= assignDef(stmt,True)
            if declaration!='':
                return 'extern '+declaration
            else:
                return ''
        else:
            return ''

    elif isinstance(stmt,ast.FunctionDef):
        return '\n\n'+functionDef(stmt,True)
    elif isinstance(stmt,ast.Expr):
        return expressionDef(stmt)
    elif isinstance(stmt,ast.Assign):
        return assignDef(stmt,False)
    elif isinstance(stmt,ast.While):
        return whileLoop(stmt)
    elif isinstance(stmt,ast.For):
        return forLoop(stmt)
    elif isinstance(stmt,ast.If):
        return ifLoop(stmt)
    elif isinstance(stmt,ast.Break):
        return 'break;'
    elif isinstance(stmt,ast.Continue):
        return 'continue;'
    elif isinstance(stmt,ast.Return):
        return 'return '+expr(stmt.value,False)+';'
    return ''


def importInC(name):
    if name in CoreModule :
        return '#include <'+name+'.h>'
    return '#include "'+name+'.h"'


def isAnInt(value):
    try: 
        int(value)
        return True
    except ValueError:
        return False

def isInt(value):
    try: 
        int(value)
        return True
    except ValueError:
        return False

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


