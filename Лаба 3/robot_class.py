from par_Class import SyntaxTreeNode
import sys
from time import sleep
def clear():
    print('\n'*10)

types = {' ': 'FLOOR',
         'X': 'WALL',
         'E': 'EXIT'}

cells = {'FLOOR': 2,
         'WALL': 1,
         'EXIT': 0}

class Cell:
    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return f'{self.type}'

class Robot:
    def __init__(self, _x=0, _y=0, _map=None):
        self.x = _x
        self.y = _y
        self.map = _map
        self.portals=[]
        self.walls = ['WALL', 'EXIT']
        self.found_exit = False

    def __repr__(self):
        return f'Robot at [{self.x}, {self.y}]\n'

    def show(self):
        for row in range(len(self.map)):
            for cell in range(len(self.map[row])):
                if self.map[row][cell].type == 'FLOOR':
                    if (cell == self.y) and (row == self.x):
                        print("@", end=' ')
                    else:
                        print(" ", end=' ')
                elif self.map[row][cell].type == 'EXIT':
                    print("E", end=' ')
                else:
                    print("X", end=' ')
            print()

    def move_top(self):
        if (self.x - 1 >= 0) and (self.map[self.x - 1][self.y].type == "FLOOR"):
            self.x -= 1
            self.show()
            clear()
            return 1
        elif (self.x - 1 >= 0) and (self.map[self.x - 1][self.y].type == "EXIT"):
            self.found_exit = True
            return 1
        else:
            return 0

    def move_bottom(self):
        if (self.x + 1 < len(self.map)) and (self.map[self.x + 1][self.y].type == "FLOOR"):
            self.x += 1
            self.show()
            clear()
            return 1
        elif (self.x + 1 < len(self.map)) and (self.map[self.x + 1][self.y].type == "EXIT"):
            self.found_exit = True
            return 1
        else:
            return 0

    def move_right(self):
        if (self.y + 1 < len(self.map[self.x])) and (self.map[self.x][self.y + 1].type == "FLOOR"):
            self.y += 1
            self.show()
            clear()
            return 1
        elif (self.x + 1 < len(self.map[self.x])) and (self.map[self.x][self.y+1].type == "EXIT"):
            self.found_exit = True
            return 1
        else:
            return 0

    def move_left(self):
        if (self.y - 1 >= 0) and (self.map[self.x][self.y - 1].type == "FLOOR"):
            self.y -= 1
            self.show()
            clear()
            return 1
        elif (self.y - 1 >= 0) and (self.map[self.x][self.y - 1].type == "EXIT"):
            self.found_exit = True
            return 1
        else:
            return 0

    def portal(self):
        coord=(self.x,self.y)
        self.portals.insert(0,coord)


    def teleport(self):
        coord=self.portals.pop(0)
        self.x=coord[0]
        self.y=coord[1]
        self.show()
        clear()

if __name__ == '__main__':
    r = Robot(0, 0)
    r.move_left()