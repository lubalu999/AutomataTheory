import sys
import par_Class
import copy
from par_Class import SyntaxTreeNode
import math
import random
from robot_class import Robot, Cell,types


class Exit(Exception):
    pass


class Value:            #переменная (инт)
    def __init__(self, symtype='' or [], value=None,write=True):
        self.type = symtype
        self.value = value
        self.write=write

    def __repr__(self):
        return f'{self.type}, {self.value}'

    def __deepcopy__(self, memodict={}):
        return Value(self.type, self.value)

    def _type(self):
        return 'Value'

class Pointer(Value):
    def __init__(self,symtype='' or [], value=None,write=True, read=True,index=0,level=0):
        Value.__init__(self, symtype, value,write)
        self.read=read
        self.index=index
        self.level=level

    def _type(self):
        return 'pointer'

    def __repr__(self):
        return f'{self.type}, {self.value}'


class Array(Value):
    def __init__(self,symtype='' or [], value=None,write=True,num=0):
        Value.__init__(self, symtype, value,write)
        self.num=num
    def __repr__(self):
        return f'{self.type}, {self.num},значение {self.value}'

    def _type(self):
        return 'Array'

#MISTAKES
class BreakStop(Exception):
    pass

class IndexError(Exception):
    pass



class MyInterpreter:

    # Initialize the interpreter. prog is a dictionary
    def __init__(self):
        self.parser = par_Class.Parser()
        self.prog = None
        self.symbol_table = [dict()]            #[Value] = ...
        self.functions = None
        self.tree = None
        self.type=[]
        self.scope = 0
        self.flagOperation=True
        self.correct=None
        self.find_exit = False
        self.robot = Robot()



    def interpreter(self,  prog=None):
        self.prog = prog            #text file
        self.tree, self.functions, self.correct = self.parser.parse(self.prog)
        if self.correct:
            self.interpreter_tree(self.tree)

            if 'main' not in self.functions.keys():
                sys.stderr.write('No main\n')
            else:
                self._main(self.functions['main'])

        else:
                sys.stderr.write(f'Can\'t intemperate incorrect input file\n')

    def interpreter_tree(self, tree):
        print("Program tree:\n")
        tree.print()
        print("\n")
        for i in self.functions.keys():
            print(i+':\n')
            self.functions[i].print()

    def interpreter_node(self, node):
        self.type.clear()

        if self.robot.found_exit:
            raise Exit
        elif '#result' in self.symbol_table[self.scope].keys():
            return

        elif node is None:
            raise Exit
        #program
        elif node.type == 'program':
            self.interpreter_node(node.children)

        #program->stategroup
        elif node.type == 'stategroup':
            for child in node.children:
                self.interpreter_node(child)

        # statement --> declaration
        elif node.type == 'declaration':
            if node.children[0].type=='type':
                self._createType(node.children[0])
            if node.children[1].type=='vars':
                children = node.children[1]
                self._declaration(children)

        #statement-->assignment
        elif node.type == 'assignment':
            try:
                self._assignment(node)
            except IndexError:
                pass
            except Exit:
                pass

        # for array assignment
        elif node.type == 'index':
            return self._index(self.symbol_table[self.scope][node.value.value],node.children)
        # binary operations
        elif node.type == 'bin_op':
            exp1=node.children[0]
            if (exp1.type != 'name') and (exp1.type != 'num'):
                exp1 = self.interpreter_node(exp1)
            exp2 = node.children[1]
            if (exp2.type != 'name') and (exp2.type != 'num'):
                exp2 = self.interpreter_node(exp2)

            if node.value == '+':               #obrabotka
                return self._plus(exp1, exp2)
            elif node.value=='-':
                return self._minus(exp1, exp2)
            elif node.value=='*':
                return self._mul(exp1,exp2)
            elif node.value=='/':
                return self._div(exp1,exp2)
            elif node.value=='%':
                return self._mod(exp1,exp2)
            elif node.value == '>=':
                return self._notLess(node.children[0], node.children[1])
            elif node.value == '<=':
                return self._notGr(node.children[0], node.children[1])
            elif node.value == '!=':
                return self._notEq(node.children[0], node.children[1])
        # unary operations
        elif node.type=='un_op':
            exp=node.children
            if node.value=='&':
                if exp.value in self.symbol_table[self.scope].keys():
                    type=copy.copy(self.symbol_table[self.scope][exp.value].type)
                    type.insert(0,'pointer')
                    return Pointer(type,exp.value,level=self.scope)
                else:
                    sys.stderr.write('Time error\n')
                    raise Exit
            elif node.value=='*':
                return self._getPointerValue(exp)
        #get Value from name node for some operations
        elif node.type=='name':
            if node.value in self.symbol_table[self.scope]:
                if self.symbol_table[self.scope][node.value].value==None:
                    sys.stderr.write(f'Cant get value of {node.value}')
                    raise Exit
                else:
                   return self.symbol_table[self.scope][node.value]
        #creat Value num from number node for operations
        elif node.type=='num':
            return Value('num',node.value)
       # statement -> return operation
        elif node.type == 'return':
            self.symbol_table[self.scope]['#result'] = self.interpreter_node(node.children)
            return
        #robot operations and sizeof and break
        elif node.type == 'operator':
            if node.value.lower() == 'top':
                return Value('num',self.robot.move_top())
            elif node.value.lower() == 'bottom':
                return Value('num',self.robot.move_bottom())
            elif node.value.lower() == 'left':
                return Value ('num',self.robot.move_left())
            elif node.value.lower() == 'right':
                return Value('num',self.robot.move_right())
            elif node.value.lower() == 'portal':
                self.robot.portal()
            elif node.value.lower() == 'teleport':
                 self.robot.teleport()
            elif node.value.lower() == 'sizeof':
                return self._sizeof(node.children)
            elif node.value.lower() == 'break':
                raise BreakStop


        #statement--> while operation
        elif node.type == 'while':
            self._while(node)
        # statement--> while operation with block finish
        elif node.type == 'while_finish':
            self._while_finish(node)
        # statement --> notzero block
        elif node.type == 'notzero?':
            self._notzero(node)
        # statement--> zero operation
        elif node.type == 'zero?':
            self._zero(node)
        # statement--> call function and return value
        elif node.type == 'function_call':
            #try:
            return self._function_call(node)
        elif node.type == 'parameters':
            for item in node.children:
                self.interpreter_node(item)
        elif node.type == 'parameter':
            self._createType(node.children)
            self._create_new_var(self.type,node.value)
        elif node.type=='foreach':
            self._foreach(node)


        # get function description
        elif node.type == 'function_description':
            pass





    # TYPE BLOCK
    def _createType(self, type: SyntaxTreeNode):
        if isinstance(type.children, SyntaxTreeNode):
            self.type.append(type.value)
            self._createType(type.children)
        elif isinstance(type.children, list):
            self.type.append(type.value)

    def check_Type(self,type):
        if type == 'value':
            return  Value(type)
        elif type == 'const value':
            return  Value(type, write=False)
        elif type == 'array of':
            return Array(type)
        elif type == 'const array of':
            return Array(type, write=False)
        elif type == 'pointer':
            return Pointer(type)
        elif type == 'const pointer':
            return Pointer(type, write=False)
        elif type == 'pointer const':
            return Pointer(type, read=False)
        elif type == 'const pointer const':
            return Pointer(type, write=False, read=False)



    def _create_new_var(self, _type: [], name: str):
        if name in self.symbol_table[self.scope].keys():
            sys.stderr.write(f'This name {name} is already exist\n')
        else:
            type = copy.copy(_type)
            if _type[0] == 'value':
                self.symbol_table[self.scope][name] = Value(type)           #scope - уровень вложенности
            elif _type[0] == 'const value':
                self.symbol_table[self.scope][name] = Value(type, write=False)
            elif _type[0] == 'array of':
                self.symbol_table[self.scope][name] = Array(type)
            elif _type[0] == 'const array of':
                self.symbol_table[self.scope][name] = Array(type, write=False)
            elif _type[0] == 'pointer':
                self.symbol_table[self.scope][name] = Pointer(type)
            elif _type[0] == 'const pointer':
                self.symbol_table[self.scope][name] = Pointer(type, write=False)
            elif _type[0] == 'pointer const':
                self.symbol_table[self.scope][name] = Pointer(type, read=False)
            elif _type[0] == 'const pointer const':
                self.symbol_table[self.scope][name] = Pointer(type, write=False, read=False)

    # DECLARATION
    def _declaration(self, node: par_Class.SyntaxTreeNode):

        if node.type == 'vars':
            for child in node.children:
                self._declaration(child)
        else:
            if node.type == 'assignment':
                self._create_new_var(self.type, node.children[0].value)
                if node.children[1].type == 'num':
                    if self.symbol_table[self.scope][node.children[0].value].type[0] == 'const value' \
                            or self.symbol_table[self.scope][node.children[0].value].type[0] == 'value':
                        self.symbol_table[self.scope][node.children[0].value].value = node.children[1].value
                    elif self.symbol_table[self.scope][node.children[0].value].type[0] == 'const array of' \
                            or self.symbol_table[self.scope][node.children[0].value].type[0] == 'array of':
                        self.symbol_table[self.scope][node.children[0].value].num = node.children[1].value

                    else:
                        sys.stderr.write(
                            f'Cant assign number to {self.symbol_table[self.scope][node.children[0].value].type}\n')
                        self.symbol_table[self.scope].pop(node.children[0].value)
                elif node.children[1].type == 'name':
                    if self.symbol_table[self.scope][node.children[1].value] is None:
                        sys.stderr.write(f'Error assignment: this var {node.children[1].value} doesnt exist\n')
                    elif self.symbol_table[self.scope][node.children[1].value].value is None:
                        sys.stderr.write(f'Error assignment: this var {node.children[1].value} is undefined\n')
                    elif (self.symbol_table[self.scope][node.children[0].value]._type()) == 'Value' and \
                            (self.symbol_table[self.scope][node.children[1].value]._type() == 'Value'):
                        self.symbol_table[self.scope][node.children[0].value].value = \
                            self.symbol_table[self.scope][node.children[1].value].value
                    elif (self.symbol_table[self.scope][node.children[0].value]._type() == 'Array') \
                            and (self.symbol_table[self.scope][node.children[1].value]._type() == 'Array'):
                        self.symbol_table[self.scope][node.children[0].value].num = \
                            self.symbol_table[self.scope][node.children[1].value].num
                        self.symbol_table[self.scope][node.children[0].value].value = \
                            copy.copy(self.symbol_table[self.scope][node.children[1].value].value)
                    elif (self.symbol_table[self.scope][node.children[0].value]._type() == 'pointer') \
                            and (self.symbol_table[self.scope][node.children[1].value]._type() == 'pointer'):
                        self.symbol_table[self.scope][node.children[0].value].value = \
                            self.symbol_table[self.scope][node.children[1].value].value
                elif node.children[1].type != 'num' and node.children[1].type != 'name':
                    val = self.interpreter_node(node.children[1])
                    if self.flagOperation == True:
                        if val._type() == 'pointer':
                            if self.symbol_table[self.scope][node.children[0].value]._type() == 'pointer':
                                self.symbol_table[self.scope][node.children[0].value].value = val.value
                            else:
                                sys.stderr.write(f'Time error\n')
                                self.symbol_table[self.scope].pop(node.children[0].value)
                        elif val._type() == 'Value':
                            if self.symbol_table[self.scope][node.children[0].value]._type() == 'Value':
                                self.symbol_table[self.scope][node.children[0].value] = Value(val.type,val.value)
                            elif self.symbol_table[self.scope][node.children[0].value]._type() == 'Array':
                                self.symbol_table[self.scope][node.children[0].value].num = val.value
                            else:
                                sys.stderr.write(f'Cant assign number to {node.children[0].value}\n')
                                self.symbol_table[self.scope].pop(node.children[0].value)
                    else:
                        sys.stderr.write(f'Expression  error\n')
                        self.flagOperation = True
                        self.symbol_table[self.scope].pop(node.children[0].value)


            else:
                if (self.type[0] != ('const value') and self.type[0] != ('const array of') and self.type[0] != ('const pointer') \
                        and self.type[0] != ('const pointer const')):
                    self._create_new_var(self.type, node.value)
                else:
                    sys.stderr.write(f'Const modification need assignment\n')

     #ASSIGNMENT
    def _assignment(self, node: SyntaxTreeNode):
        variable = node.children[0]
        expression = node.children[1]
        flag=True
        tab=None
        if variable.type=='pointer_variable':
            if variable.children.type!='name':
                var=self.interpreter_node(variable.children)
            else:
                var=self.symbol_table[self.scope][variable.children.value]
            exp=self.interpreter_node(expression)
            vv=self.symbol_table[var.level][var.value]
            if vv._type()=='Value' or vv._type()=='pointer':
                vv.value=copy.deepcopy(exp)
            elif vv._type()=='Array':
                vv.value[var.index]=copy.copy(exp)
            return
        elif variable.type=='index':
            if variable.value.value in self.symbol_table[self.scope].keys():
                if  self.symbol_table[self.scope][variable.value.value]._type()=='Array':
            #проверка на массив
                   tab=self._index(self.symbol_table[self.scope][variable.value.value],variable.children)

        elif variable.value not in self.symbol_table[self.scope].keys():
            sys.stderr.write(f'Undeclared symbol\n')
            raise Exit

        elif self.symbol_table[self.scope][variable.value].write==False:
                   sys.stderr.write(f'Const var {variable.value}\n')
                   raise Exit
        else:
            tab = self.symbol_table[self.scope][variable.value]
        if tab is None:
            raise Exit

        if expression.type=='name':
           if  expression.value not in self.symbol_table[self.scope].keys():
              sys.stderr.write(f'Undeclared symbol\n')
              raise Exit
           elif (tab._type()=='Value' and (self.symbol_table[self.scope][expression.value]._type()=='Value'))\
                        or (tab._type()=='pointer' and (self.symbol_table[self.scope][expression.value]._type()=='pointer')):
                    tab=copy.copy(self.symbol_table[self.scope][expression.value])
           elif (tab._type()=='Array') and (self.symbol_table[self.scope][expression.value]._type()=='Array'):
               tab.value=copy.deepcopy(self.symbol_table[self.scope][expression.value].value)
           else:
               sys.stderr.write('Assign error\n')
               raise Exit
        elif expression.type=='num':
            if (tab._type()=='Value'):
                tab.value = expression.value
            else:
                sys.stderr.write(f'Error assignment num to {tab.type[0]}l\n')
                raise Exit
        elif expression.type!='num' or 'name':
            var=self.interpreter_node(expression)
            if self.flagOperation==True:
                if var._type()=='pointer' and (tab._type()=='pointer' and tab.write==True and tab.read==True):
                    if len(tab.type)>=2:
                        if isinstance(var.value,str):
                            if (var.type==tab.type):
                                tab.value=var.value
                                tab.level=var.level
                                tab.index=var.index
                            else:
                                sys.stderr.write(f'Type Error Assign\n')
                                raise Exit
                        else:
                            if var.type==tab.type:
                                tab.value = var.value
                                tab.level=var.level
                            else:
                                sys.stderr.write(f'Type Error Assign \n')
                                raise Exit
                    else:
                        if len(tab.type)==1:
                            tab.value = copy.copy(var.value)


                elif (var._type()=='Value') and (tab._type()=='Value' and tab.write==True):
                    tab.value = var.value
                else:
                    sys.stderr.write('Cant assign different types\n')
                    raise Exit
            else:
                self.flagOperation=True
    #INDEX BLOCK FOR ARRAY TYPE
    def _index(self, val: Array, node: SyntaxTreeNode):
        if isinstance(node,SyntaxTreeNode):
            if node.type == 'last_index':
                expr=node.children
                value=self.interpreter_node(expr).value
                index=self._index_index(val,value)
                return  index
            elif node.type == 'index':
                expr = node.children[0]
                value = self.interpreter_node(expr).value
                val=self._index_index(val,value)
                return self._index(val,node.children[1])
            else:
                sys.stderr.write(f'Index error\n')
                raise IndexError



    def _index_index(self,val : Array, value : int):
        if val==None:
           sys.stderr.write('Index Error!\n')
           raise IndexError
        elif not isinstance(val.value, list):
            if (val.write == False) and (val.num == 0):
                sys.stderr.write('Time error\n')
                raise IndexError
            elif len(val.type) == 1:
                val.value = [Value('value', None)]
            elif len(val.type) >= 2:
                if val.type[1] == 'array of':
                    val.value = [Array(val.type[1:], None)]
                elif val.type[1] == 'pointer':
                    val.value = [Pointer(val.type[1:], None)]
            if value == 0:
                return val.value[0]  # создала массив и возвращаю присовение 0
            else:
                sys.stderr.write(f'Index error\n')
                raise IndexError
        else:
            if len(val.value) == value:
                if val.write:  # если массив не статический (нижняя граница?)
                    if val.value[0]._type()=='Array':
                        val.value.append(Array(val.value[0].type))
                    elif val.value[0]._type() == 'Value':
                        val.value.append(Value(val.value[0].type))
                    elif val.value[0]._type()=='pointer':
                        val.value.append(Pointer(val.value[0].type))
                    return val.value[value]
                else:
                    if val.num > value:
                        if val.value[0]._type() == 'Array':
                            val.value.append(Array(val.value[0].type))
                        elif val.value[0]._type() == 'Value':
                            val.value.append(Value(val.value[0].type))
                        elif val.value[0]._type() == 'pointer':
                            val.value.append(Pointer(val.value[0].type))
                        return val.value[value]
                    else:
                        sys.stderr.write(f'Index error\n')
                        raise IndexError
            elif len(val.value)>value:
                return val.value[value]
            else:
                sys.stderr.write(f'Index error\n')
                raise IndexError


     #BINARY OPERATIONS
    def _plus(self, exp1: SyntaxTreeNode or Value, exp2: SyntaxTreeNode or Value):
        type1=''
        type2=''
        val1=0
        val2=0
        if isinstance(exp1,SyntaxTreeNode):
            if exp1.type=='name':
                if self.symbol_table[self.scope][exp1.value].value!=None:
                    type1=self.symbol_table[self.scope][exp1.value]._type()
                    val1=self.symbol_table[self.scope][exp1.value].value
                    exp1=self.symbol_table[self.scope][exp1.value]
                else:
                    sys.stderr.write(f'Illigial operation: var  {exp1.value} does not have value\n')
                    self.flagOperation=False
                    return Value('num',1)
            elif exp1.type=='num':
                type1='num'
                val1=exp1.value
                exp1=Value(type1,val1)
        else:
            type1 = exp1._type()
            val1 = exp1.value
        if isinstance(exp2,SyntaxTreeNode):
            if exp2.type=='name':
                if self.symbol_table[self.scope][exp2.value].value != None:
                    type2 = self.symbol_table[self.scope][exp2.value]._type()
                    val2 = self.symbol_table[self.scope][exp2.value].value
                    exp2=self.symbol_table[self.scope][exp2.value]
                else:
                    sys.stderr.write(f'Illigial operation: var  {exp2.value} does not have value\n')
                    self.flagOperation = False
                    return Value('num', 1)
            elif exp2.type=='num':
                type2='num'
                val2=exp2.value
                exp2=Value(type2,val2)
        else:
            type2=exp2._type()
            val2=exp2.value

        if (type1=='Value' or type1== 'num') and  (type2=='Value' or type2=='num'):
            return Value('num',val1+val2)
        elif (type1=='pointer' and (type2=='Value' or type2=='num')):
            if len(exp1.type)>=2:
                if exp1.type[1]=='array of':
                    val=exp1.index+val2
                    arr=self.symbol_table[exp1.level][exp1.value]
                    if len(arr.value) > val:
                        ttype = copy.copy(arr.type)
                        ttype.insert(0, 'pointer')
                        return Pointer(ttype, exp1.value, index=val)
                    elif len(arr.value) == val:
                        arr.value.append(Value('num'))
                        ttype = copy.copy(arr.type)
                        ttype.insert(0, 'pointer')
                        return Pointer(ttype, exp1.value, index=val)
                    else:
                        sys.stderr.write('Time error\n')
                        raise Exit
            else:
                sys.stderr.write('Error pointer sum\n')
                self.flagOperation=False
                return Value('num',1)
        elif (type2=='pointer' and  (type1=='Value' or type1=='num')):
            if len(exp2.type) >= 2:
                if exp2.type[1] == 'array of':
                    val = exp2.index + val2
                    arr = self.symbol_table[exp2.level][exp2.value]
                    if len(arr.value) > val:
                        ttype = copy.copy(arr.type)
                        ttype.insert(0, 'pointer')
                        return Pointer(ttype, exp2.value, index=val)
                    else:
                        sys.stderr.write('Time error\n')
                        raise Exit
            else:
                sys.stderr.write('Error pointer sum\n')
                self.flagOperation = False
                return Value('num', 1)

        elif (type1=='Array' or type2=='Array'):
            sys.stderr.write(f'Cant plus with type array of\n')
            self.flagOperation = False
            return Value('num', 1)
        else:
            sys.stderr.write(f'Unknown error\n')
            self.flagOperation = False
            return Value('num', 1)

    def _minus(self, exp1: SyntaxTreeNode, exp2: SyntaxTreeNode):
        type1 = ''
        type2 = ''
        val1 = 0
        val2 = 0
        if isinstance(exp1, SyntaxTreeNode):
            if exp1.type == 'name':
                if self.symbol_table[self.scope][exp1.value].value != None:
                    type1 = self.symbol_table[self.scope][exp1.value]._type()
                    val1 = self.symbol_table[self.scope][exp1.value].value
                    exp1 = self.symbol_table[self.scope][exp1.value]
                else:
                    sys.stderr.write(f'Illigial operation: var  {exp1.value} does not have value\n')
                    self.flagOperation = False
                    return Value('num', 1)
            elif exp1.type == 'num':
                type1 = 'num'
                val1 = exp1.value
                exp1 = Value(type1, val1)
        else:
            type1 = exp1._type()
            val1 = exp1.value
        if isinstance(exp2, SyntaxTreeNode):
            if exp2.type == 'name':
                if self.symbol_table[self.scope][exp2.value].value != None:
                    type2 = self.symbol_table[self.scope][exp2.value]._type()
                    val2 = self.symbol_table[self.scope][exp2.value].value
                    exp2 = self.symbol_table[self.scope][exp2.value]
                else:
                    sys.stderr.write(f'Illigial operation: var  {exp2.value} does not have value\n')
                    self.flagOperation = False
                    return Value('num', 1)
            elif exp2.type == 'num':
                type2 = 'num'
                val2 = exp2.value
                exp2 = Value(type2, val2)
        else:
            type2 = exp2._type()
            val2 = exp2.value

        if (type1 == 'Value' or type1 == 'num') and (type2 == 'Value' or type2 == 'num'):
            return Value('num', val1 - val2)
        elif (type1 == 'pointer' and (type2 == 'Value' or type2 == 'num')):
            if len(exp1.type) >= 2:
                if exp1.type[1] == 'array of':
                    val = exp1.index - val2
                    arr = self.symbol_table[exp1.level][exp1.value]
                    if len(arr.value) > val:
                        ttype = copy.copy(arr.type)
                        ttype.insert(0, 'pointer')
                        return Pointer(ttype, exp1.value, index=val)
                    else:
                        sys.stderr.write('Time error\n')
                        raise Exit
            else:
                sys.stderr.write('Error pointer minus\n')
                self.flagOperation = False
                return Value('num', 1)
        elif (type2 == 'pointer' and (type1 == 'Value' or type1 == 'num')):
            if len(exp2.type) >= 2:
                if exp2.type[1] == 'array of':
                    val = exp2.index - val2
                    arr = self.symbol_table[exp2.level][exp2.value]
                    if len(arr.value) > val:
                        ttype = copy.copy(arr.type)
                        ttype.insert(0, 'pointer')
                        return Pointer(ttype, exp2.value, index=val)
                    else:
                        sys.stderr.write('Time error\n')
                        raise Exit
            else:
                sys.stderr.write('Error pointer minus\n')
                self.flagOperation = False
                return Value('num', 1)

        elif (type1 == 'Array' or type2 == 'Array'):
            sys.stderr.write(f'Cant minus with type array of\n')
            self.flagOperation = False
            return Value('num', 1)
        else:
            sys.stderr.write(f'Unknown error\n')
            self.flagOperation = False
            return Value('num', 1)

    def _mul(self, exp1: SyntaxTreeNode, exp2: SyntaxTreeNode):
        type1=''
        type2=''
        val1=0
        val2=0
        if exp1.type == 'name':
            if self.symbol_table[self.scope][exp1.value].value != None:
                type1 = self.symbol_table[self.scope][exp1.value]._type()
                val1 = self.symbol_table[self.scope][exp1.value].value
            else:
                sys.stderr.write(f'Illigial operation: var  {exp1.value} does not have value\n')
                self.flagOperation = False
                return Value('num', 1)
        else:
            type1 = 'num'
            val1 = exp1.value
        if exp2.type == 'name':
            if self.symbol_table[self.scope][exp2.value].value != None:
                type2 = self.symbol_table[self.scope][exp2.value]._type()
                val2 = self.symbol_table[self.scope][exp2.value].value
            else:
                sys.stderr.write(f'Illigial operation: var  {exp2.value} does not have value\n')
                self.flagOperation = False
                return Value('num', 1)
        else:
            type2 = 'num'
            val2 = exp2.value
        #For VALUE
        if (type1 == 'Value' or type1 == 'num') or (type2 == 'Value' or type1 == 'num'):
            return Value('num', val1*val2)
        #FOR POINTER
        elif (type1=='pointer') or (type2=='pointer'):
            sys.stderr.write(f'Cant multiplication with type pointer\n')
            self.flagOperation = False
            return Value('num', 1)
        #FOR ARRAY
        elif (type1=='Array' or type2=='Array'):
            sys.stderr.write(f'Cant multiplication with type array of\n')
            self.flagOperation = False
            return Value('num', 1)
        else:
            sys.stderr.write(f'Unknown error\n')

    def _div(self, exp1: SyntaxTreeNode, exp2: SyntaxTreeNode):
        type1=''
        type2=''
        val1=0
        val2=0
        if exp1.type=='name':
            if self.symbol_table[self.scope][exp1.value].value!=None:
                type1=self.symbol_table[self.scope][exp1.value]._type()
                val1=self.symbol_table[self.scope][exp1.value].value
            else:
                sys.stderr.write(f'Illigial operation: var  {exp1.value} does not have value\n')
                self.flagOperation = False
                return Value('num', 1)
        else:
            type1='num'
            val1=exp1.value
        if exp2.type=='name':
            if self.symbol_table[self.scope][exp2.value].value != None:
                type2 = self.symbol_table[self.scope][exp2.value]._type()
                val2 = self.symbol_table[self.scope][exp2.value].value
            else:
                sys.stderr.write(f'Illigial operation: var  {exp2.value} does not have value\n')
                self.flagOperation = False
                return Value('num', 1)
        else:
            type2 = 'num'
            val2=exp2.value

        if val2 == 0:
            sys.stderr.write(f'Zero divison\n')
            self.flagOperation = False
            return Value('num', 1)
        else:
            #FOR VALUE
            if (type1=='Value' or type1=='num') and  (type2=='Value' or type2== 'num'):
                    return Value('num',int(val1/val2))
            #FOR POINTER
            elif (type1=='pointer') or (type2=='pointer'):
                sys.stderr.write(f'Cant div with type pointer\n')
                self.flagOperation = False
                return Value('num', 1)
            #FOR ARRAY
            elif (type1=='Array' or type2=='Array'):
                sys.stderr.write(f'Cant div with type array of\n')
                self.flagOperation = False
                return Value('num', 1)
            else:
                sys.stderr.write(f'Unknown error\n')
                self.flagOperation = False
                return Value('num', 1)

    def _mod(self, exp1: SyntaxTreeNode, exp2: SyntaxTreeNode):
        type1=''
        type2=''
        val1=0
        val2=0
        if exp1.type=='name':
            if self.symbol_table[self.scope][exp1.value].value!=None:
                type1=self.symbol_table[self.scope][exp1.value]._type()
                val1=self.symbol_table[self.scope][exp1.value].value
            else:
                sys.stderr.write(f'Illigial operation: var  {exp1.value} does not have value\n')
                self.flagOperation = False
                return Value('num', 1)
        else:
            type1='num'
            val1=exp1.value
        if exp2.type=='name':
            if self.symbol_table[self.scope][exp2.value].value != None:
                type2 = self.symbol_table[self.scope][exp2.value]._type()
                val2 = self.symbol_table[self.scope][exp2.value].value
            else:
                sys.stderr.write(f'Illigial operation: var  {exp2.value} does not have value\n')
                self.flagOperation = False
                return Value('num', 1)
        else:
            type2 = 'num'
            val2=exp2.value

        if val2 == 0:
            sys.stderr.write(f'Zero divison\n')
            self.flagOperation = False
            return Value('num', 1)
        else:
            #FOR VALUE
            if (type1=='Value' or type1=='num') and  (type2=='Value' or type2=='num'):
                    return Value('num',int(val1 % val2))
            #FOR POINTER
            elif (type1=='pointer') or (type2=='pointer'):
                sys.stderr.write('Cant % with type pointer\n')
                self.flagOperation = False
                return Value('num', 1)
            #FOR ARRAY
            elif (type1=='Array' or type2=='Array'):
                sys.stderr.write(f'Cant  % with type array of\n')
                self.flagOperation = False
                return Value('num', 1)
            else:
                sys.stderr.write(f'Unknown error\n')
                self.flagOperation = False
                return Value('num', 1)

    def _notLess(self,exp1: SyntaxTreeNode,exp2:SyntaxTreeNode):
        exp1=self.interpreter_node(exp1)
        if exp1==None:
            sys.stderr.write('Wrong compare\n')
            raise Exit
        exp2 = self.interpreter_node(exp2)
        if exp2==None:
            sys.stderr.write('Wrong compare\n')
            raise Exit
        if  exp1._type()=='Value' and  exp2._type()=='Value':
            f=bool(exp1.value >= exp2.value)
            if f:
                return Value('num',1)
            else:
                return Value('num',0)

        else:
            sys.stderr.write('Cant compare\n')
            return Value(value=None)

    def _notGr(self, exp1: SyntaxTreeNode, exp2: SyntaxTreeNode):
        exp1 = self.interpreter_node(exp1)
        if exp1==None:
            sys.stderr.write('Wrong compare\n')
            raise Exit

        exp2 = self.interpreter_node(exp2)
        if exp2 == None:
            sys.stderr.write('Wrong compare\n')
            raise Exit
        if exp1._type()=='Value' and  exp2._type()=='Value':
            f = bool(exp1.value <= exp2.value)
            if f:
                return Value('num', 1)
            else:
                return Value('num', 0)
        else:
            sys.stderr.write('Cant compare\n')
            return Value(value=None)

    def _notEq(self,exp1: SyntaxTreeNode, exp2 :SyntaxTreeNode):

        exp1 = self.interpreter_node(exp1)
        if exp1==None:
            sys.stderr.write('Wrong compare\n')
            raise Exit


        exp2 = self.interpreter_node(exp2)
        if exp2 == None:
            sys.stderr.write('Wrong compare\n')
            raise Exit
        if  exp1._type()=='Value' and  exp2._type()=='Value':
            f = bool(exp1.value != exp2.value)
            if f:
                return Value('num', 1)
            else:
                return Value('num', 0)
        else:
            sys.stderr.write('Cant compare\n')
            return Value(value=None)

    #UNARY OPERATION WITH POINTER
    def _getPointerValue(self,node: SyntaxTreeNode):
        tab=self.interpreter_node(node)#вернет объект одного из класса
        if isinstance(tab,Pointer): #проверили что разименовываем укзаатель
           name=tab.value #получаем имя объекта который надо разименовать
           if name in self.symbol_table[tab.level]:
               var=self.symbol_table[tab.level][name]
               if var._type() == 'Array':
                    if isinstance(var.value, list) and tab.index<len(var.value):
                       return var.value[tab.index]
                    else:
                        sys.stderr.write('Cant get value\n')
                        raise Exit
               elif var._type()=='Value':
                    if var.value:
                        return Value('num',var.value)
                    else:
                        sys.stderr.write('Cant get value\n')
                        raise Exit
               elif var._type()=='pointer':
                    return var
           else:
               sys.stderr.write(f'Undecleared symbol\n')
               raise Exit

        else:
            sys.stderr.write(f'Not pointer. Cant get value of {node.value}\n')
            raise Exit

    #WHILE BLOCK
    def _while(self, node: SyntaxTreeNode):

        while True:
            try:
                condition = self.interpreter_node(node.children['condition']).value
                if condition >= 1:
                    self.interpreter_node(node.children['body'])
                else:
                    break
            except BreakStop:
                self.flagOperation=False
                break
    def _while_finish(self, node: SyntaxTreeNode):

        while True:
                self._while(node.children['while'])
                if self.flagOperation:
                    self.interpreter_node(node.children['finish'])
                else:
                    self.flagOperation=True
                break

    #ZERO BLOCK
    def _notzero(self, node: SyntaxTreeNode):

            condition = self.interpreter_node(node.children['condition']).value
            if condition != 0:
                self.interpreter_node(node.children['body'])

    def _zero(self,node: SyntaxTreeNode):
            condition = self.interpreter_node(node.children['condition']).value
            if condition == 0:
                self.interpreter_node(node.children['body'])

    # FOREACH BLOCK
    def _foreach(self, node: SyntaxTreeNode):
        if node.value in self.symbol_table[self.scope].keys():
            if self.symbol_table[self.scope][node.value]._type() == 'Array':
                k = 0
                for i in self.symbol_table[self.scope][node.value].value:
                    self.symbol_table[self.scope][node.value].value[k] = self._function_call(node.children, True, i)
                    k += 1
            else:
                self.symbol_table[self.scope][node.value] = self._function_call(node.children, True,
                                                                                self.symbol_table[self.scope][
                                                                                    node.value])
        else:
            sys.stderr.write('Error variable in foreach\n')

    #FUNCTION BLOCK


    def _main(self, node: SyntaxTreeNode):
        try:
            self.interpreter_node(node.children['body'])
        except Exit:
            pass




    def _function_call(self, node: SyntaxTreeNode,flag=False, each=0):
        name=node.value
        func_node=None
        params =[]
        if name not in self.functions.keys():
            sys.stderr.write('Function call Error')
            return
        else:
            func_node=self.functions[node.value]
        if name=='main':
            sys.stderr.write('Interpretator Error')
            return
        #input parametrs
        parameters=[]
        if flag==True:
            parameters.append(each)
        if (node.children['parametrs'] is not None):
            self._parametrs(node.children['parametrs'].children,parameters)
        """Adding for recursion checking"""
        if '#' + name not in self.symbol_table[0].keys():
            self.symbol_table[0]['#' + name] = 1
        else:
            self.symbol_table[0]['#' + name] += 1
        if self.symbol_table[0]['#' + name] > 1000:
            self.symbol_table.pop()
            self.scope -= 1
            sys.stderr.write('Recursion error\n')
            raise Exit

        #GET PARAMETRS
        self.scope+=1       #увеличиваем то что спустились ниже
        self.symbol_table.append(dict())        #переопределяем словарь
        if func_node is not None:
            self.interpreter_node(func_node.children['parametrs'])
        else:
            sys.stderr.write('Function call Error')
            self.symbol_table.pop()
        #CHECK PARAMETERS   функции
        if len(parameters)==len(self.symbol_table[self.scope]):
            k=0
            for i in self.symbol_table[self.scope].keys():
                if parameters[k]._type()==self.symbol_table[self.scope][i]._type():
                    self.symbol_table[self.scope][i].value=parameters[k].value
                    k+=1
                else:
                    sys.stderr.write('Function call Error\n')
                    self.symbol_table.pop()
                    self.scope -= 1
        else:
            sys.stderr.write('Function call Error\n')
            self.symbol_table.pop()
            self.scope-=1

        #MAKE BODY
        self.interpreter_node(func_node.children['body'])     #родитель предложений для этой функции
        #CHECK RESULT
        if '#result' in self.symbol_table[self.scope].keys():
            if self.symbol_table[self.scope]['#result']._type()==self.check_Type(func_node.children['type'].value)._type():
                result= self.symbol_table[self.scope]['#result']
                self.symbol_table.pop()
                self.scope -= 1
                return result
            else:
                sys.stderr.write('Function call Error\n')
                self.symbol_table.pop()
                self.scope -= 1
                raise Exit
        else:
            sys.stderr.write('Function call Error\n')
            self.symbol_table.pop()
            self.scope -= 1
            raise Exit


    def _parametrs(self, node: list or SyntaxTreeNode, vars: list):
        if isinstance(node, list):
            self._parametrs(node[0], vars)
            value = self.interpreter_node(node[1])
            if value == None:
                sys.stderr.write('Error parametrs\n')
            else:
                vars.append(copy.copy(value))
        else:
            if node.type == 'call parameters':
                self._parametrs(node.children, vars)
            else:
                value = self.interpreter_node(node)
                if value == None:
                    sys.stderr.write('Error parametrs\n')
                else:
                    vars.append(copy.copy(value))

    #OPERATORS BLOCK к массиву
    def _sizeof(self, node :SyntaxTreeNode):
        expr = self.interpreter_node(node)
        if expr._type()=='Value' or  expr._type()=='pointer':
            return Value('num',1)
        elif expr._type()=='Array' and expr.value!=None:
            return Value('num',len(expr.value))
        elif  expr._type()=='Array' and expr.value==None:
            return Value('num',0)
        else:
            sys.stderr.write("Size of error\n")
            return


    def print_symbol(self):
        print(self.symbol_table)

    def create_robot(self,name):
        fl = open(name)
        _text = fl.readlines()
        robot_info = _text.pop(0).rstrip().split(" ")
        map_size = _text.pop(0).rstrip().split(" ")

        # robot set
        x = int(robot_info[0])
        y = int(robot_info[1])
        _map = [0] * int(map_size[0])

        for i in range(int(map_size[0])):
            _map[i] = [0] * int((map_size[1]))
        for i in range(int(map_size[0])):
            for j in range(int(map_size[1])):
                _map[i][j] = Cell("EMPTY")
        pos = 0
        for i in range(int(map_size[0])):
            line = list(_text.pop(0).rstrip())
            line = [Cell(types[i]) for i in line]
            _map[pos] = line
            pos += 1
        self.robot = Robot(_x=x, _y=y, _map=_map)



if __name__ == '__main__':
    f=open('algorithm', 'r')
    txt=f.read()
    f.close()
    #txt='value b=4;\n pointer a=&b;\nb=2;\nvalue c=*a;\n'
    interpr=MyInterpreter()

    interpr.create_robot('mmmaaapp')
    interpr.robot.show()
    interpr.interpreter(prog=txt)
    interpr.print_symbol()
