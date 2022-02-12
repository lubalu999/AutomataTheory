from SMC import AutomataAnalyzer
import time
import os.path

def SMCconsolecheck(str):
    try:
        statemachine = AutomataAnalyzer.AutomataAnalyzer()
        match = statemachine.Check(str)
        if match:
            return str.rstrip('\n') + ' --- Correct'
        else:
            return str.rstrip('\n') + ' --- Incorrect'
    except Exception:
        return str.rstrip('\n') + ' --- Incorrect'

def SMCfilecheck():
    statemachine = AutomataAnalyzer.AutomataAnalyzer()
    inf = open('strings.txt', 'r')
    ouf = open('SMCoutput.txt', 'w')

    _dict = {}
    _starttime = time.time()
    for line in inf.readlines():
        match = statemachine.Check(line)
        if match:
            _dict[statemachine.GetName()] = statemachine.GetNumOfElems()
    _endtime = time.time()

    for k in _dict:
        ouf.write(k + ' - ' + str(_dict[k]) + '\n')

    if os.path.isfile('time.txt'):
        timefile = open('time.txt', 'a')
        timefile.write('Analyzing with SMC completed in ' + str(_endtime - _starttime) + ' seconds\n')
    else:
        timefile = open('time.txt', 'w')
        timefile.write('Analyzing with SMC completed in ' + str(_endtime - _starttime) + ' seconds\n')

    timefile.close()
    inf.close()
    ouf.close()