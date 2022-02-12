import sys
import ply.lex as lex

class Lexer():
    def __init__(self):
        self.lexer=lex.lex(module=self)

    tokens = (
        'VALUE', 'ARRAYOF', 'WHILE', 'FINISH', 'POINTER', 'NAME',
        'CONST', 'COMMA', 'SIZEOF', 'NL', 'PLUS', 'MINUS', 'STAR', 'ASSIGNMENT',
        'PERCENT', 'SLASH', 'OBRACKET', 'CBRACKET', 'OFBRACKET', 'CFBRACKET', 'OSQBRACKET', 'CSQBRACKET',
        'AMPERSAND', 'ZERO', 'NOTZERO', 'TOP', 'NUMBER',
        'BOTTOM', 'LEFT', 'RIGHT', 'PORTAL', 'TELEPORT', 'MAIN', 'RETURN',
        'SEMICOLON', 'BREAK', 'NOTLESS', 'NOTGREATER', 'NOTEQ', 'FOREACH'
    )

    t_ignore = ' \t'
    def token(self):
        return self.lexer.token()

    def t_COMMA(self, t):
        r'\,'
        return t

    def t_VALUE(self, t):
        r'value(?!\w)'
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_SLASH(self, t):
        r'\/'
        return t

    def t_ARRAYOF(self, t):
        r'array\ of(?!\w)'
        return t

    def t_WHILE(self, t):
        r'while(?!\w)'
        return t

    def t_FINISH(self, t):
        r'finish(?!\w)'
        return t

    def t_POINTER(self, t):
        r'pointer(?!\w)'
        return t

    def t_CONST(self, t):
        r'const(?!\w)'
        return t

    def t_SIZEOF(self, t):
        r'sizeof(?!\w)'
        return t

    def t_OBRACKET(self, t):
        r'\('
        return t

    def t_CBRACKET(self, t):
        r'\)'
        return t

    def t_OSQBRACKET(self, t):
        r'\['
        return t

    def t_CSQBRACKET(self, t):
        r'\]'
        return t

    def t_OFBRACKET(self, t):
        r'\{'
        return t

    def t_CFBRACKET(self, t):
        r'\}'
        return t

    def t_ASSIGNMENT(self, t):
        r'='
        return t

    def t_RETURN(self, t):
        r'return(?!\w)'
        return t

    def t_ZERO(self, t):
        r'zero\?(?!\w)'
        return t

    def t_NOTZERO(self, t):
        r'notzero\?(?!\w)'
        return t

    def t_PLUS(self, t):
        r'\+'
        return t

    def t_MINUS(self, t):
        r'\-'
        return t

    def t_AMPERSAND(self, t):
        r'&'
        return t

    def t_STAR(self, t):
        r'\*'
        return t

    def t_PERCENT(self, t):
        r'\%'
        return t

    def t_FOREACH(self, t):
        r'foreach(?!\w)'
        return t

    def t_BREAK(self, t):
        r'break(?!\w)'
        return t

    def t_SEMICOLON(self, t):
        r'\;'
        return t

    def t_MAIN(self, t):
        r'main(?!\w)'
        return t

    def t_TOP(self, t):
        r'top(?!\w)'
        return t

    def t_BOTTOM(self, t):
        r'bottom(?!\w)'
        return t

    def t_LEFT(self, t):
        r'left(?!\w)'
        return t

    def t_RIGHT(self, t):
        r'right(?!\w)'
        return t

    def t_PORTAL(self, t):
        r'portal(?!\w)'
        return t

    def t_TELEPORT(self, t):
        r'teleport(?!\w)'
        return t

    def t_NOTLESS(self, t):
        r'\>='
        return t

    def t_NOTGREATER(self, t):
        r'\<='
        return t

    def t_NOTEQ(self, t):
        r'\!='
        return t

    def t_NAME(self, t):
        r'[a-zA-Z][a-zA-Z_0-9]*'
        '''save the type?'''
        return t

    def t_NL(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')
        return t

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(len(t.value))

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


if __name__ == '__main__':
    f = open('algorithm')
    data = f.read()
    f.close()
    lexer = Lexer()
    lexer.test(data)

    