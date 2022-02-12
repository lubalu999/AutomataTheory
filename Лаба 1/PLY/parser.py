from PLY import lexer
import PLY.yacc as yacc


class Parser:
    tokens = lexer.Lexer.tokens

    def __init__(self):
        self._lexer = lexer.Lexer()
        self._parser = yacc.yacc(module=self, optimize=1, debug=False, write_tables=False)
        self._stats = {}
        self.name = ''
        self.count = 0
        self.flag = False


    def p_array(self, p):
        """array : NAME SIZE EQUAL ELEMS NL"""
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5]
        self.name = p[1]
        _size_str = p[2].lstrip('[')
        _size_str = _size_str.rstrip(']')
        _elems_str = p[4].lstrip('{')
        _elems_str = _elems_str.rstrip('}')
        if len(_size_str) != 0:
            if int(_size_str) != 0:
                _size = int(_size_str)
                self.count = _size
            else:
                _size = -1
                self.count = _size
        else:
            _size = 0
            self.count = _size
        if len(_elems_str) != 0:
            _realsize = len(_elems_str.split(','))
        else:
            _realsize = 0

        if _size >= _realsize or _size == 0 and _realsize > 0:
            self.flag = True
            if _size == -1 and _realsize == 0 or _size == 0 and _realsize == 0:
                self.flag = False
            #if self._stats.get(p[2]):
            #    self._stats[p[2]][1] = True
            #else:
            #    self._stats[p[2]] = [p[1].strip(), False]

    def p_array_zero_error(self, p):
        """array : err NL"""
        p[0] = p[1] + p[2]

    def p_array_first_error(self, p):
        """array : NAME err NL"""
        p[0] = p[1] + p[2] + p[3]

    def p_array_second_error(self, p):
        """array : NAME SIZE err NL"""
        p[0] = p[1] + p[2] + p[3] + p[4]

    def p_array_third_error(self, p):
        """array : NAME SIZE EQUAL err NL"""
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5]

    def p_err(self, p):
        """err : UNKNOWN"""
        p[0] = p[1]

    def p_error(self, p):
        pass

    def PLYCheck(self, _str, _file = False):
        if _file == False:
            self._stats.clear()
        self.flag = False
        _res = self._parser.parse(_str)
        return _str