import re
import time
import os.path

#def checkfromconsole():
#    while True:
#        _string = input()
#        if _string == 'stop':
#            break
#        if check(_string):
#            print(_string, '   --- Correct')
#        else:
#            print(_string, '   --- Incorrect')
#        print('Enter \'stop\' to stop entering strings')

def check(_str):
    _str1 = _str.strip(' ')
    _reg = r"^([a-zA-Z][0-9a-zA-Z]{0,15})(\[)([0-9]{0,9})?(\])(\=)(\{)((\-{0,1}[0-9]+\,){0,}\-{0,1}[0-9]+)?(\})$"

    _res = re.match(_reg, _str1)

    if _res is not None:
        if _res.group(7):
            _buf = _res.group(7).split(',')
        else:
            _buf = []
            if _res.group(3) == '' or int(_res.group(3)) == 0:
                return _str1 + '   --- Incorrect'
        if _res.group(3):
            _number = int(_res.group(3))
            if _number < len(_buf):
                return _str1 + '   --- Incorrect'
            else:
                return _str1 + '   --- Correct'
        else:
            return _str1 + '   --- Correct'


def checkfromgeneratedfile():
    inf = open('strings.txt', 'r')
    ouf = open('REGEXoutput.txt', 'w')
    _dict = {}
    _starttime = time.time()
    while True:
        _string = inf.readline()
        if not _string:
            break
        _reg = r"^([a-zA-Z][0-9a-zA-Z]{0,15})(\[)([0-9]{0,9})?(\])(\=)(\{)((\-{0,1}[0-9]+\,){0,}\-{0,1}[0-9]+)?(\})$"
        _str = _string
        _res = re.match(_reg, _str)

        if _res is not None:
            if _res.group(7):
                _buf = _res.group(7).split(',')
            else:
                _buf = []
                if _res.group(3) == '' or int(_res.group(3)) == 0:
                    continue
            if _res.group(3):
                _number = int(_res.group(3))
                if _number < len(_buf):
                    continue
                else:
                    _dict[_res.group(1)] = _number
            else:
                _dict[_res.group(1)] = ''
    _endtime = time.time()

    for k in _dict:
        ouf.write(k + ' - ' + str(_dict[k]) + '\n')

    if os.path.isfile('time.txt'):
        timefile = open('time.txt', 'a')
        timefile.write('Analyzing with Regex completed in ' + str(_endtime - _starttime) + ' seconds\n')
    else:
        timefile = open('time.txt', 'w')
        timefile.write('Analyzing with Regex completed in ' + str(_endtime - _starttime) + ' seconds\n')

    timefile.close()
    inf.close()
    ouf.close()

#checkfromgeneratedfile()
#checkfromconsole()



