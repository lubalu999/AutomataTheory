from PLY import parser
import time
import os.path

def PLYconsolecheck(_str):
    _parser = parser.Parser()
    _str += '\n'
    _res = _parser.PLYCheck(_str)
    if _parser.flag:
        return _str.rstrip('\n') + ' --- Correct\n'
    else:
        return _str.rstrip('\n') + ' --- Incorrect\n'


def PLYfilecheck():
    _parser = parser.Parser()
    inf = open('strings.txt', 'r')
    ouf = open('PLYoutput.txt', 'w')

    _dict = {}
    _starttime = time.time()
    for line in inf.readlines():
        _res = _parser.PLYCheck(line, _file=True)
        if _parser.flag:
            _dict[_parser.name] = _parser.count
    _endtime = time.time()

    for k in _dict:
        ouf.write(k + ' - ' + str(_dict[k]) + '\n')

    if os.path.isfile('time.txt'):
        timefile = open('time.txt', 'a')
        timefile.write('Analyzing with PLY completed in ' + str(_endtime - _starttime) + ' seconds\n')
    else:
        timefile = open('time.txt', 'w')
        timefile.write('Analyzing with PLY completed in ' + str(_endtime - _starttime) + ' seconds\n')

    timefile.close()
    inf.close()
    ouf.close()