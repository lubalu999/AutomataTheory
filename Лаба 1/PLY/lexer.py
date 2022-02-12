import re
import PLY.lex as lex

class Lexer:
    states = (
        #('type', 'exclusive'),
        #('name', 'exclusive'),
        ('size', 'exclusive'),
        ('elements', 'exclusive')
    )

    tokens = (
        'NAME',
        'SIZE', 'EQUAL', 'ELEMS',
        'NL', 'UNKNOWN'
    )

    #t_INITIAL = r''
    #t_NAME = r'(?i)([a-z]([a-z0-9]){0,15})'
    #t_SIZE = r'\[([0-9]{0,9})?\]'
    #t_EQUAL = r'\='
    #t_ELEMS = r'\{((\-{0,1}[0-9]+\,)*(\-{0,1}[0-9]+))?\}'

    t_ANY_ignore = ''


    def __init__(self):
        self.lexer = lex.lex(module=self)

    def input(self, data):
        return self.lexer.input(data)

    def token(self):
        return self.lexer.token()


    def t_NAME(self, t):
        r'([a-zA-Z]([a-zA-Z0-9]){0,15})'
        t.lexer.begin('size')
        return t

    def t_size_SIZE(self, t):
        r'\[([0-9]{1,9})?\]'
        return t

    def t_size_EQUAL(self, t):
        r'\='
        t.lexer.begin('elements')
        return t

    def t_elements_ELEMS(self, t):
        r'\{((\-{0,1}[0-9]+\,)*(\-{0,1}[0-9]+))?\}'
        return t

    def t_ANY_NL(self, t):
        r'\s*(\n)'
        t.lexer.lineno += len(t.value)
        t.lexer.begin('INITIAL')
        return t

    def t_ANY_UNKNOWN(self, t):
        r'(.)+'
        #print("Illegal character '%s'" % t.value[0])
        t.lexer.begin('INITIAL')
        return t

    def t_ANY_error(self, t):
        # print("Illegal character '%s' " % t.value[0])
        t.lexer.skip(1)
        t.lexer.begin('INITIAL')
        return t