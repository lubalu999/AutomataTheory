from inter_Class import MyInterpreter
menu = ['1. Value Test',
        '2. Array Test',
        '3. Pointer Test',
        '4. Sort',
        '5. Factorial recursion',
        '6. Factorial with foreach construct',
        '7. Errors',
        '8. Robot',
        '0. Exit']

errors_menu=['1.Syntax error',
             '2.Const errors',
             '3.The same function name',
             '4. Functions without main',
             '0. Exit']

robot_menu=['1. Test move',
            '2. Test algorithm',
            '3. Test right hand while',
            '4. Test right hand recursion',
            '5. New algorythm',
            '0. Exit']

if __name__ == '__main__':
    while True:
        print('Choose your fighter:')
        for i in menu:
            print(i)
        k=int(input())
        if k==0:
            print('Have a good day :)')
            break
        elif k==1:
            f = open('tests/check_value', 'r')
            txt = f.read()
            print('Input:\n', txt)
            f.close()
            interpr = MyInterpreter()
            interpr.interpreter(prog=txt)
            interpr.print_symbol()
        elif k==2:
            f = open('tests/check_array', 'r')
            txt = f.read()
            print('Input:\n', txt)
            f.close()
            interpr = MyInterpreter()
            interpr.interpreter(prog=txt)
            interpr.print_symbol()
        elif k==3:
            f = open('tests/check_pointer', 'r')
            txt = f.read()
            print('Input:\n', txt)
            f.close()
            interpr = MyInterpreter()
            interpr.interpreter(prog=txt)
            interpr.print_symbol()
        elif k==4:
            f = open('tests/sort', 'r')
            txt = f.read()
            print('Input:\n', txt)
            f.close()
            interpr = MyInterpreter()
            interpr.interpreter(prog=txt)
            interpr.print_symbol()
        elif k==5:
            f = open('tests/factorial', 'r')
            txt = f.read()
            print('Input:\n', txt)
            f.close()
            interpr = MyInterpreter()
            interpr.interpreter(prog=txt)
            interpr.print_symbol()
        elif k==6:
            f = open('tests/foreach', 'r')
            txt = f.read()
            print('Input:\n', txt)
            f.close()
            interpr = MyInterpreter()
            interpr.interpreter(prog=txt)
            interpr.print_symbol()
        elif k==7:
            while True:
                print('Choose your fighter:')
                for i in errors_menu:
                    print(i)
                kk = int(input())
                if kk == 0:
                    break
                elif kk==1:
                    f = open('tests/syntax_error', 'r')
                    txt = f.read()
                    print('Input:\n', txt)
                    f.close()
                    interpr = MyInterpreter()
                    interpr.interpreter(prog=txt)
                    interpr.print_symbol()
                elif kk == 2:
                    f = open('tests/check_errors_const', 'r')
                    txt = f.read()
                    print('Input:\n', txt)
                    f.close()
                    interpr = MyInterpreter()
                    interpr.interpreter(prog=txt)
                    interpr.print_symbol()
                elif kk == 3:
                    f = open('tests/check_errors_func', 'r')
                    txt = f.read()
                    print('Input:\n', txt)
                    f.close()
                    interpr = MyInterpreter()
                    interpr.interpreter(prog=txt)
                    interpr.print_symbol()
                elif kk == 4:
                    f = open('tests/check_func_2', 'r')
                    txt = f.read()
                    print('Input:\n', txt)
                    f.close()
                    interpr = MyInterpreter()
                    interpr.interpreter(prog=txt)
                    interpr.print_symbol()
        elif k == 8:
            while True:
                print('Choose your fighter:')
                for i in robot_menu:
                    print(i)
                p = int(input())
                if p == 0:
                    break
                elif p==1:
                    f = open('tests/move', 'r')
                    txt = f.read()
                    print('Input:\n', txt)
                    f.close()
                    interpr = MyInterpreter()
                    interpr.create_robot('tests/map_2_0')
                    interpr.interpreter(prog=txt)
                    interpr.print_symbol()
                elif p==2:
                    f=open('tests/algorithm','r')
                    txt=f.read()
                    print('Input:\n', txt)
                    f.close()
                    interpr = MyInterpreter()
                    interpr.create_robot('tests/mmmaaapp')
                    interpr.interpreter(prog=txt)
                    interpr.print_symbol()
                elif p==3:
                    f = open('tests/hand_while', 'r')
                    txt = f.read()
                    print('Input:\n', txt)
                    f.close()
                    interpr = MyInterpreter()
                    interpr.create_robot('tests/big_map')
                    interpr.interpreter(prog=txt)
                    interpr.print_symbol()

                elif p==4:
                    f = open('tests/hand', 'r')
                    txt = f.read()
                    print('Input:\n', txt)
                    f.close()
                    interpr = MyInterpreter()
                    interpr.create_robot('tests/map')
                    interpr.interpreter(prog=txt)
                    interpr.print_symbol()
                elif p==5:
                    f = open('tests/algo_2', 'r')
                    txt = f.read()
                    print('Input:\n', txt)
                    f.close()
                    interpr = MyInterpreter()
                    interpr.create_robot('tests/big_map')
                    interpr.interpreter(prog=txt)
                    interpr.print_symbol()