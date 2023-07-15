'''
Converts infix expression to postfix.
Limitation: input needs to be correctly spaced.
Author: krpelenio
Date: July 15, 2023
'''

import sys
import re
from operator import itemgetter, attrgetter

symbol_table = []
token_table = []
file = ""
code_dec = ""
code_init = ""
code_perf = ""

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)


class Symbol():
    #stores symbols
    def __init__(self, data_type, var, value):
        self.var = var
        self.data_type = data_type
        self.value = value

class Token():
    #stores tokens and lexemes
    def __init__(self, token, lexeme):
        self.token = token
        self.lexeme = lexeme

def parse():
    global code_dec
    global code_init
    global code_perf

    #divides code into DEC, INIT, and DEC parts
    code = file.splitlines()
    start_dec = 0
    start_init = 0
    start_perf = 0
    for i in range(len(code)):
        if(code[i] == "DECLARE"):
            start_dec = i
        elif(code[i] == "INITIALIZE"):
            start_init = i
        elif(code[i] == "PERFORM"):
            start_perf = i


    code_dec = code[1:start_init-1]
    code_init = code[start_init+1:start_perf-1]
    code_perf = code[start_perf+1:len(code)]
    parse_declare()
    parse_initialize()
    parse_perform()

def parse_declare():
    global symbol_table
    global code_dec
    for i in range(len(code_dec)):
        has_error = False
        line = code_dec[i].split(' ')

        #check for declaration errors in type and # of parameters
        for index, value in enumerate(symbol_table):
            if value.var == line[0]:
                print('Declaration Error: Variable name already used')
                has_error = True

        if len(line) != 2:
            print('Declaration Error: Line has too many parameters')
            has_error = True
        
        if all( [line[0]!='int', line[0]!='bool', line[0]!='str'] ):
            print('Declaration Error: Incorrect type')
            has_error = True

        #save declarations in symbol table
        if(has_error == False):
            symbol_table.append(Symbol(line[0],line[1],None))
    #viewall()

def parse_initialize():
    global symbol_table
    global code_init
    var_type = ''
    temp_string = ''

    for i in range(len(code_init)):
        has_error = False
        var_exist = False
        line = code_init[i].split(' ')

        #check for declaration errors in type and # of parameters
        for index, value in enumerate(symbol_table):
            #print('value.var: ', value.var)
            #print('line[0]: ', line[0])
            if value.var == line[0]:
                var_type = value.data_type
                var_exist = True

        if var_exist == False:
            print("Error:", code_init[i])
            print('Initialization Error: Variable not declared.')
            has_error = True

        if var_type == 'int' and is_int(line[1]) == False:
            print("Error:", code_init[i])
            print('Initialization Error: Value should be integer.')
            has_error = True

        elif var_type == 'bool' and is_bool(line[1]) == False:
            print("Error:", code_init[i])
            print('Initialization Error: Value should be boolean.')
            has_error = True

        elif var_type == 'str':
            for index in range(1,len(line)):
                temp_string += line[index]
                if(index < len(line)-1):
                    temp_string += " "
            line[1] = temp_string
            line = line[:2]
            if(is_str(line[1]) == False):
                print("Error:", code_init[i])
                print('Initialization Error: Value should be a string.')
                has_error = True

        if(has_error == False):
            for index, value in enumerate(symbol_table):
                #print('value.var: ',value.var)
                #print('line[0]: ',line[0])
                if value.var == line[0]:
                    value.value = line[1]
        else:
             sys.exit()
    viewall()

def is_int(value):
    is_int = True
    try:
        val = int(value)
    except ValueError:
        is_int = False
    return is_int

def is_bool(value):
    is_bool = True
    if all([value!= 'true', value!= 'false']):
        is_bool = False
    return is_bool

def is_str(value):
    is_str = True
    if any([value[0]!= '$', value[-1]!= '$', bool(re.search('\$', value[1:-1]))]):
        is_str = False
    return is_str

def parse_perform():
    print('perform function:')
    global symbol_table
    global code_perf
    eval_output = 0
    for i in range(len(code_perf)):
        has_error = False
        var_exist = False
        line = code_perf[i].split(' ')
        if getType(line)=='expression':
            output = convertToPostfix(code_perf[i])
            eval_output = eval_postfix(output)
            print(eval_output)
        else:
            print('else')


def getType(line):
    line_type = 'Invalid'
    if(line[0]=='[' and line[-1]==']'):
        line_type = 'input'
    elif(len(line)== 1):
        line_type = 'string'
    else:
        line_type = 'expression'
    return line_type
        

def convertToPostfix(expr):
    op_prec = {}
    op_prec["."] = 4 #exponentiation
    op_prec["*"] = 3 #multiplication
    op_prec["/"] = 3 #division
    op_prec["#"] = 3 #remainder/modulo
    op_prec["+"] = 2 #addition
    op_prec["-"] = 2 #subtraction
    op_prec["("] = 1 #open parenthesis
    op_prec[")"] = 1 #close parenthesis
    opStack = Stack()
    postfixList = []
    tokenList = expr.split(' ')
    print (tokenList)
    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "abcdefghijklmnopqrstuvwxyz" or token.isdigit():
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (op_prec[opStack.peek()] >= op_prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    print (postfixList)
    return postfixList

def eval_postfix(text):
    global symbol_table
    s = list()
    symbol_value = None
    for symbol in text:
        print("symbol: ", symbol)
        result = None
        if symbol.isdigit():
            s.append(int(symbol))
        elif is_var(symbol):
            var_value = get_var_value(symbol)
            #print("VAR VALUE: ", var_value)
            s.append(var_value)
        elif is_operator(symbol) and len(s) != 0:
            operand1 = int(s.pop())
            operand2 = int(s.pop())
            if symbol == "+":
                result = round(operand1 + operand2)
            elif symbol == "-":
                result = round(operand1 - operand2)
            elif symbol == ".":
                result = round(operand1 * operand2)
            elif symbol == "/": 
                result = round(operand2 / operand1)
        if result!= None:
            print(result)
            s.append(result)
        #else:
             #print("unknown value %s"%symbol)
    #print("PRINT")
    #for p in s: print (p)
    return s.pop()

def is_var(varname):
     global symbol_table
     var_value = False
     for item in symbol_table:
         if (item.var == varname) and (is_operator(varname)==False):
              return True

def get_var_value(varname):
     global symbol_table
     for item in symbol_table:
          if (item.var == varname) and (is_operator(varname)==False):
               return item.value

def is_empty(s):
     is_empty = False
     if not s:
          is_empty = True

     return is_empty

def is_operator(token):
     is_operator = False
     if token in "+-./~^#" or token in ">=<!":
          is_operator = True

     return is_operator
     
    
def execute():
    print('execute')
def symboltable():
    print('symbol')
def tokentable():
    print('token')

def viewall():
    global symbol_table
    print("VIEW ALL")
    for value in symbol_table:
        print(value.var)
        print(value.data_type)
        print(value.value)

#TODO: Fix the file input
#filename = input("Enter name of file to be interpreted: ")
#f = open(filename, 'r')
#f = open('test1.dip', 'r')
#file = f.read()
#print(file)
#parse()

#print(convertToPostfix("A . B + C . D"))
#print(convertToPostfix("( A + B ) . C - ( D - E ) . ( F + G )"))
print(convertToPostfix("( A + B ) * ( C * D - E ) * F / G"))   # A B + C D * E – * F * G /
