import random
import string


def makerndstr(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(size))


def makernddigitstr(size):
    return ''.join(random.choice(string.digits) for i in range(size))


def generate(_num, _lengh = 0):
    timef = open('time.txt', 'a')
    timef.write('Number of strings: ' + str(_num) + '\n')
    timef.close()
    if _lengh != 0 :
        with open('strings.txt', 'w') as ouf:
            for i in range(_num):
                bufstr = ''
                if random.randint(1, 4) > 3:
                    bufstr += makerndstr(random.randint(0, 2))
                _name = random.choice(string.ascii_letters)
                _name += makerndstr(random.randint(0, 2))
                bufstr += _name
                if random.randint(0, 100) < 91:
                    bufstr += '['
                else:
                    bufstr += '{'
                if random.randint(0, 100) > 95:
                    _size = makernddigitstr(random.randint(0, 17))
                else:
                    _size = str(random.randint(0, 9))
                bufstr += _size
                if random.randint(0, 10) < 9:
                    bufstr += ']'
                else:
                    bufstr += ')'
                if random.randint(0, 10) < 9:
                    bufstr += '='
                else:
                    bufstr += '+'
                if random.randint(0, 10) < 9:
                    bufstr += '{'
                else:
                    bufstr += '('

                for i in range(100):
                    _dg = str(random.randint(0, 999))
                    bufstr += _dg
                    if len(bufstr) >= _lengh:
                        break
                    if i != 100 - 1:
                        if random.randint(0, 100) < 98:
                            bufstr += ','
                        else:
                            bufstr += '; '

                if random.randint(0, 10) < 9:
                    bufstr += '}'
                else:
                    bufstr += ')'
                ouf.write(bufstr + '\n')
    else:
        with open('strings.txt', 'w') as ouf:
            for i in range(_num):
                bufstr = ''
                if random.randint(1, 4) > 3:
                    bufstr += makerndstr(random.randint(0, 2))
                _name = random.choice(string.ascii_letters)
                _name += makerndstr(random.randint(0, 2))
                bufstr += _name
                if random.randint(0, 100) < 91:
                    bufstr += '['
                else:
                    bufstr += '{'
                if random.randint(0, 100) > 95:
                    _size = makernddigitstr(random.randint(0, 17))
                else:
                    _size = str(random.randint(0, 9))
                bufstr += _size
                if random.randint(0, 10) < 9:
                    bufstr += ']'
                else:
                    bufstr += ')'
                if random.randint(0, 10) < 9:
                    bufstr += '='
                else:
                    bufstr += '+'
                if random.randint(0, 10) < 9:
                    bufstr += '{'
                else:
                    bufstr += '('
                if random.randint(0, 100) < 91:
                    if _size != '' and _size != '0' and int(_size) < 30:
                        k = int(_size)
                    else:
                        k = 0
                else:
                    k = random.randint(0, 20)
                for i in range(k):
                    _dg = str(random.randint(0, 999999))
                    bufstr += _dg
                    if i != k - 1:
                        if random.randint(0, 100) < 98:
                            bufstr += ','
                        else:
                            bufstr += '; '
                if random.randint(0, 10) < 9:
                    bufstr += '}'
                else:
                    bufstr += ')'
                ouf.write(bufstr + '\n')
    ouf.close()
