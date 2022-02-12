import regex
import generator
import os.path
from SMC import SMC_Check
from SMC import AutomataAnalyzer
from PLY import PLY_Check

while True:
    print('1. Generate new file')
    print('2. Check file with RegEx')
    print('3. Check file with SMC')
    print('4. Check file with PLY')
    print('5.- Enter string from keyboard')
    print('6.- Show time of analyzing')
    print('7.- Clear time statistics')
    print('0. Quit')
    print('Make your choice: ')

    c = input()
    if c.isdigit():
        choice = int(c)
        if choice == 1:
            print('How many strings do you want to have in a new file?: ')
            while True:
                numstr = input()
                if numstr.isdigit():
                    num = int(numstr)
                    break
                else:
                    print('Wrong choice, try again!')
            print('How long will the lines be? (0 - without length): ')
            while True:
                line = input()
                if line.isdigit():
                    length = int(line)
                    break
                else:
                    print('Wrong choice, try again!')
            generator.generate(num, length)
        elif choice == 2:
            regex.checkfromgeneratedfile()
        elif choice == 3:
            SMC_Check.SMCfilecheck()
        elif choice == 4:
            PLY_Check.PLYfilecheck()
        elif choice == 5:
            print('Enter the string: ')
            str = input()
            if regex.check(str) is not None:
                print('RegEx result:', regex.check(str))
            else:
                print('RegEx result: ' + str + '   --- Incorrect')
            if SMC_Check.SMCconsolecheck(str) is not None:
                print('SMC  result:', SMC_Check.SMCconsolecheck(str))
            else:
                print('SMC  result: ' + str + '   --- Incorrect')
            print('PLY  result:', PLY_Check.PLYconsolecheck(str))

        elif choice == 6:
            if os.path.isfile('time.txt'):
                times = open('time.txt', 'r')
                for line in times.readlines():
                    print(line.rstrip('\n'))
                print('\n')
                times.close()
            else:
                print('Sorry, but you haven\'t analyzed file yet')
        elif choice == 7:
            times = open('time.txt', 'w')
            times.close()
        elif choice == 0:
            break
        else:
            print('Wrong choice, try again!')
    else:
        print('Wrong choice, try again!')
print('The end!')