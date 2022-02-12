import ply.yacc as yacc
from lex_Class import Lexer
from ply.lex import LexError
import sys
from typing import List, Dict, Tuple


class SyntaxTreeNode:
    def __init__(self, _type='', value=None, children=None, lineno=None):
        self.type = _type
        self.value = value
        self.children = children or []
        self.lineno = lineno

    def __repr__(self):
        return f"""{self.type}: {self.value or ''} {self.lineno or ''}"""

    def print_(self, level: int = 0):
        print(' ' * level, self)

    def print(self, level: int = 0):
        if self is None:
            return
        print('->' * level, self)
        if isinstance(self.children, list):
            for child in self.children:
                if child:
                    child.print(level + 1)
        elif isinstance(self.children, SyntaxTreeNode):
            self.children.print(level + 1)
        elif isinstance(self.children, dict):
            for key, value in self.children.items():
                print('->' * (level + 1), key)
                if value:
                    value.print(level + 2)


class Parser():
    tokens = Lexer.tokens

    precedence = (
        ('nonassoc', 'NOTLESS', 'NOTGREATER', 'NOTEQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'PERCENT', 'SLASH', 'STAR',),
        ('left', 'ASSIGNMENT'),
        ('right', 'AMPERSAND')
    )

    def __init__(self):
        self._lexer = Lexer()
        self.parser = yacc.yacc(module=self)
        self.functions = dict()
        self.ok = True

    def parse(self, s):
        try:
            res = self.parser.parse(s)
            return res, self.functions, self.ok
        except LexError:
            sys.stderr.write(f'Illegal token {s}\n')

    def p_program(self, p):
        '''program : stategroup'''
        p[0] = SyntaxTreeNode('program', children=p[1], lineno=p.lineno(1))

    # функция типа : value main/name_1 (array of pointer a) {группа предложениий}

    # не уверена на счет ошибки выглядит как параша ))))

    # группа предложений
    def p_stategroup(self, p):
        '''stategroup :  stategroup statement
                    | statement'''
        if len(p) == 2:
            p[0] = SyntaxTreeNode('stategroup', children=[p[1]])
        else:
            p[0] = SyntaxTreeNode('stategroup', children=[p[1], p[2]])

    # это различные варианты предложений от объявления (значение a, ...) до выражения возврата: return a + b;
    def p_statement(self, p):               #p0 p1 p2 p3...
        '''statement :  declaration SEMICOLON  NL
                    | assignment SEMICOLON NL
                    | while NL
                    | zero  NL
                    | function NL
                    | operator SEMICOLON NL
                    | RETURN expression SEMICOLON
                    | foreach SEMICOLON NL
                    | empty NL'''
        if p[1] == 'return':
            p[0] = SyntaxTreeNode('return', children=p[2], lineno=p.lineno(1))
        else:
            p[0] = p[1]

    def p_statement_error(self, p):             #обработка ошибок
        '''statement : declaration  error
                    | assignment error
                    | while error
                    | zero  error
                    | function error
                    | operator error
                    | RETURN expression error'''
        p[0] = SyntaxTreeNode('error', value="Wrong statement", lineno=p.lineno(1))
        sys.stderr.write(f'>>> Wrong statement\n')
        self.ok = False

    # это нормальный тип + некоторая переменная

    def p_declaration(self, p):         #объявдение
        '''declaration : type vars'''
        p[0] = SyntaxTreeNode('declaration', children=[p[1], p[2]])

    def p_declaration_error(self, p):
        """declaration : type error"""
        p[0] = SyntaxTreeNode('declaration', value=p[1], children=p[2], lineno=p.lineno(2))
        sys.stderr.write(f'>>> Wrong name of declared value\n')
        self.ok = False

    def p_vars_icv(self, p):
        '''vars : NAME COMMA vars'''
        p[0] = SyntaxTreeNode('vars',
                              children=[SyntaxTreeNode('name', value=p[1], lineno=p.lineno(1)),
                                        p[3]])

    # a=2*v, a

    def p_vars_acv(self, p):
        '''vars : assignment_var COMMA vars'''
        p[0] = SyntaxTreeNode('vars', children=[p[1], p[3]])

    # только один или конец списка переменных

    def p_vars_name(self, p):
        '''vars : NAME'''
        p[0] = SyntaxTreeNode('vars', children=[SyntaxTreeNode('name', value=p[1], lineno=p.lineno(1))])

    # same

    def p_vars(self, p):
        '''vars : assignment_var '''
        p[0] = SyntaxTreeNode('vars', children=[p[1]])

    def p_assignment_var(self, p):
        '''assignment_var : variable ASSIGNMENT expression'''
        p[0] = SyntaxTreeNode('assignment', children=[p[1], p[3]], lineno=p.lineno(1))

    def p_assignment(self, p):
        '''assignment : assignment_var
        | pointer ASSIGNMENT expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = SyntaxTreeNode('assignment', children=[p[1], p[3]], lineno=p.lineno(1))

    def p_assignment_err(self, p):
        '''assignment : variable ASSIGNMENT error'''
        p[0] = SyntaxTreeNode('error', value="Wrong assignment", lineno=p.lineno(1))
        sys.stderr.write(f'>>> Wrong assignment\n')
        self.ok = False

    def p_pointer(self, p):
        '''pointer : STAR NAME
                  | STAR OBRACKET expression CBRACKET'''
        if len(p) == 5:
            p[0] = SyntaxTreeNode('pointer_variable', children=p[3])
        else:
            p[0] = SyntaxTreeNode('pointer_variable', children=SyntaxTreeNode('name', value=p[2]))

    def p_variable(self, p):
        '''variable : NAME
         | variable index'''
        if len(p) == 2:
            p[0] = SyntaxTreeNode('name', p[1], lineno=p.lineno(1))
        else:
            p[0] = SyntaxTreeNode('index', p[1], children=p[2], lineno=p.lineno(2))

    def p_index(self, p):
        """index : OSQBRACKET expression CSQBRACKET index
                    | OSQBRACKET expression CSQBRACKET"""
        if len(p) == 5:
            p[0] = SyntaxTreeNode('index', children=[p[2], p[4]], lineno=p.lineno(2))
        else:
            p[0] = SyntaxTreeNode('last_index', children=p[2], lineno=p.lineno(2))

    # different type of variable
    # чет какие то деревья понастроила хз хз шо за параша
    def p_type(self, p):
        ''' type : VALUE
        | CONST VALUE
        | POINTER expr_type
        | CONST POINTER expr_type
        | POINTER CONST expr_type
        | CONST POINTER CONST expr_type
        | ARRAYOF expr_type
        | CONST ARRAYOF expr_type
        '''
        if len(p) == 2:
            p[0] = SyntaxTreeNode('type', value=p[1], lineno=p.lineno(1))
        elif (len(p) == 3 and p[1] == 'const'):
            p[0] = SyntaxTreeNode('type', value=p[1] + ' ' + p[2])

        elif len(p) == 3 and p[1] != 'value':
            p[0] = SyntaxTreeNode('type', value=p[1], children=p[2])

        elif len(p) == 4:
            p[0] = SyntaxTreeNode('type', value=p[1] + ' ' + p[2], children=p[3])

        elif len(p) == 5:
            p[0] = SyntaxTreeNode('type', value=p[1] + ' ' + p[2] + ' ' + p[3], children=p[4])

    # надо ли добавлять константные значения? this is type expression
    def p_expr_type(self, p):
        ''' expr_type :
        | VALUE
        | POINTER expr_type
        | ARRAYOF expr_type
        '''
        if len(p) == 2:
            p[0] = SyntaxTreeNode('type', value=p[1], lineno=p.lineno(1))
        elif len(p) == 3:
            p[0] = SyntaxTreeNode('type', value=p[1], children=p[2], lineno=p.lineno(1))

    def p_expression(self, p):  # al_expression stands for Arithmetical-Logical
        '''expression : variable
        | al_expression
        | function_call
        | operator
        | SIZEOF OBRACKET variable CBRACKET'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = SyntaxTreeNode('operator', p[1], children=p[3], lineno=p.lineno(1))

    def p_al_expression(self, p):
        '''al_expression : expression PLUS expression
        | expression MINUS expression
        | expression PERCENT expression
        | expression STAR expression
        | expression SLASH expression
        | STAR expression
        | AMPERSAND expression
        | expression NOTGREATER expression
        | expression NOTLESS expression
        | expression NOTEQ expression
        | NUMBER'''
        if len(p) == 3:
            p[0] = SyntaxTreeNode('un_op', p[1], children=p[2], lineno=p.lineno(1))
        elif len(p) == 4:
            p[0] = SyntaxTreeNode('bin_op', p[2], children=[p[1], p[3]], lineno=p.lineno(1))
        else:
            p[0] = SyntaxTreeNode('num', value=p[1])

    def p_al_expression_group(self, p):
        'al_expression : OBRACKET al_expression CBRACKET'
        p[0] = p[2]

    def p_operator(self, p):
        '''operator : TOP
        | BOTTOM
        | LEFT
        | RIGHT
        | PORTAL
        | TELEPORT
        | BREAK
        | SIZEOF OBRACKET al_expression CBRACKET'''
        if len(p) == 2:
            p[0] = SyntaxTreeNode('operator', p[1], lineno=p.lineno(1))
        else:
            p[0] = SyntaxTreeNode('operator', p[1], children=p[2], lineno=p.lineno(1))

    def p_while_finish(self, p):
        '''while : while FINISH OFBRACKET  NL stategroup  CFBRACKET'''
        p[0] = SyntaxTreeNode('while_finish', children={'while': p[1], 'finish': p[5]}, lineno=p.lineno(1))

    def p_while(self, p):
        '''while : WHILE OBRACKET expression CBRACKET  OFBRACKET  NL stategroup  CFBRACKET'''
        p[0] = SyntaxTreeNode('while', children={'condition': p[3], 'body': p[7]}, lineno=p.lineno(1))

    def p_while_error(self, p):
        '''while : WHILE error'''
        p[0] = SyntaxTreeNode('error', value="Wrong while", lineno = p.lineno(1))
        sys.stderr.write(f'>>> Wrong while\n')
        self.ok = False

    def p_zero(self, p):
        ''' zero : ZERO  OBRACKET expression CBRACKET  OFBRACKET  NL stategroup  CFBRACKET
              | NOTZERO OBRACKET expression CBRACKET  OFBRACKET  NL stategroup  CFBRACKET
              | ZERO  OBRACKET expression CBRACKET  NL statement
              | NOTZERO OBRACKET expression CBRACKET  NL statement
        '''
        if len(p) == 9:
            p[0] = SyntaxTreeNode(p[1], children={'condition': p[3], 'body': p[7]}, lineno = p.lineno(1))
        else:
            p[0] = SyntaxTreeNode(p[1], children={'condition': p[3], 'body': p[6]}, lineno = p.lineno(1))

    def p_zero_error(self, p):
        ''' zero : ZERO error
        | NOTZERO error
        '''
        p[0] = SyntaxTreeNode('error', value = "Wrong zero", lineno = p.lineno(1))
        sys.stderr.write(f'>>> Wrong zero\n')
        self.ok = False

    def p_function(self, p):
        '''function : type funcname OBRACKET parameters CBRACKET  OFBRACKET  NL stategroup  CFBRACKET
                    | type funcname OBRACKET  CBRACKET OFBRACKET NL stategroup CFBRACKET'''
        if p[2] in self.functions:
            sys.stderr.write(f'>>> function name duplicate at {p.lineno(2)} line\n')
            self.ok = False
        else:

            if len(p) == 10:
                self.functions[p[2]] = SyntaxTreeNode('function',
                                                      children={'type': p[1], 'parametrs': p[4], 'body': p[8]})
                p[0] = SyntaxTreeNode('function_description', value = [2])
            elif len(p) == 9:
                self.functions[p[2]] = SyntaxTreeNode('function',
                                                      children={'type': p[1], 'parametrs': None, 'body': p[7]})
                p[0] = SyntaxTreeNode('function_description', value = p[2])

    def p_function_error(self, p):
        '''function : type funcname error'''
        p[0] = SyntaxTreeNode('error', value="Wrong function", lineno=p.lineno(1))
        sys.stderr.write(f'>>> Wrong function \n')
        self.ok = False

    def p_funcname(self, p):
        '''funcname : MAIN
                     | NAME'''
        p[0] = p[1]

    def p_foreach(self, p):
        '''foreach : FOREACH NAME function_call'''
        p[0] = SyntaxTreeNode('foreach', p[2], children = p[3], lineno = p.lineno(1))

    def p_foreach_error(self, p):
        'foreach : FOREACH error'
        sys.stderr.write(f'>>> Wrong foreach type\n')
        self.ok = False

    def p_function_call(self, p):
        'function_call : NAME OBRACKET call_parameters CBRACKET '
        p[0] = SyntaxTreeNode('function_call', p[1], children={'parametrs': p[3]}, lineno=p.lineno(1))

    def p_call_parameters(self, p):
        '''call_parameters :
                 | call_parameters COMMA expression
                 | expression'''
        if len(p) == 2:
            p[0] = SyntaxTreeNode('call parameters', children = p[1], lineno = p.lineno(1))
        elif len(p) == 4:
            p[0] = SyntaxTreeNode('call parameters', children = [p[1], p[3]], lineno = p.lineno(1))

    def p_parameters(self, p):
        """parameters : parameters COMMA parameter
                      | parameter"""
        if len(p) == 2:
            p[0] = SyntaxTreeNode('parameters', children=[p[1]])
        else:
            p[0] = SyntaxTreeNode('parameters', children=[p[1], p[3]])

    def p_parameter(self, p):
        """parameter : type NAME"""
        p[0] = SyntaxTreeNode('parameter', value=p[2], children=p[1])

    def p_empty(self, p):
        'empty : '
        p[0] = SyntaxTreeNode('empty')

    def p_error(self, p):
        if not p:
            print(f'Syntax error \n')
            self.ok = False


if __name__ == '__main__':
    parser = Parser()
    f = open('algorithm', 'r')
    txt = f.read()
    f.close()
    tree, functions,ok = parser.parse(txt)

    if tree is not None and ok is True:
        tree.print()
        print(functions)
        functions['main'].print()
    else:
        print('error tree built')