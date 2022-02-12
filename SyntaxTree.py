import networkx as nx
import matplotlib.pyplot as plt
from itertools import groupby

meta = ['|', '?', '*', '.']  # {}, ()
eclist = {'*' : '@', '?' : '#', '.' : '_', '|' :  '+'}
reveclist = {'@' : '*', '#' : '?', '_' : '.', '+' :  '|'}


class Node:
    def __init__(self, val='', left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def countbrackets(string):
    j = 0
    k = 0  # для прохода по строке по индексам
    for i in string:
        if j < 0:
            return False
        if i == '(':
            j += 1
        elif i == ')':
            j -= 1
        elif i == '{' and string[k - 1] in meta or i == '}' and string[k - 1] == '{':  # *{}, ?{}, |{}
            return False
        else:
            pass
        k += 1
    if j == 0:
        return True
    else:
        return False


def isOr(string):
    i = 0
    j = 0
    for k in string:
        if k == '(':
            j += 1
        if k == ')':
            j -= 1
        if (k == '|') and (j == 0):
            return i
        i += 1
    return None


def FindEnd(string):
    j = 1
    i = 0
    flag = 0
    end = 1
    t = 1
    if isOr(string) != None:
        return isOr(string)
    if string[0] != '(':
        for k in range(len(string)):
            if string[k] == '(':
                flag = 1
            elif string[k] == '|' and flag == 0:
                return i
            elif string[k] == ')':
                flag = 0
            i += 1
        if i == len(string):
            return 1
        else:
            return i - 1
    while j > 0:
        if string[t] == '(':
            j += 1
        if string[t] == ')':
            j -= 1
        t += 1
    end = t
    return end


def ClearString(string):
    while FindEnd(string) == len(string) and len(string) > 2:
        string = string[1:-1]
        #print(string)
    return string


def printTree(node, level=0):
    if node != None:
        printTree(node.left, level + 1)
        if node.val in reveclist.keys():
            print(' ' * 4 * level + '->', reveclist[node.val])
        else:
            print(' ' * 4 * level + '->', node.val)
        printTree(node.right, level + 1)

def reverseTree(tree):
    if tree != None:
        temp = tree.right
        tree.right = tree.left
        tree.left = temp
        reverseTree(tree.left)
        reverseTree(tree.right)

def copy(string):
    flag = 0
    cnt = 1
    end = 0
    if string[0] == '(':
        end = FindEnd(string)
        if string[end] == '{':
            i = end + 1
            count = ''
            while string[i] != '}':
                count += string[i]
                i += 1
            lenght = len(count) + 2  # {} и то что внцтри
            count = int(count)
            new_str = '(' + string[: end] * count + ')' + string[end + lenght:]
            return new_str
        else:
            return string

    else:
        while flag == 0 and (string[end + 1] not in meta) and end < len(string) - 2 and (string[end + 1] != '{') and (
                string[end + 1] != '('):
            end += 1
        if string[end + 1] == '{':
            i = end + 2
            count = ''
            while string[i] != '}':
                count += string[i]
                i += 1
            lenght = len(count) + 2  # {} и то что внцтри
            count = int(count)
            new_str = '(' + string[: end + 1] * count + ')' + string[end + lenght + 1:]
            return new_str
        else:
            return string

def PrepareString(string, eclist):
    for i in eclist.keys():
        string = string.replace('%'+i+'%', eclist[i])
    for i in range(len(string)):
        groupped_str = groupby(string[i:])
        for elem, grouper in groupped_str:
            k = int(len(list(grouper)))
            if (elem in ['*', '?']):
                if k > 1:
                    string = string.replace(elem*k, elem)
    return string

class SyntaxTree:

    def __init__(self):
        self.tree = Node('root', None, None)
        self.root = self.tree
        self.GraphRoot = None           #типы класса GraphNode
        self.GraphEnd = None
        self.G = nx.DiGraph()
        self.count = 0
        self.Gedges = {}

    def BuildTree(self, string, currentnode=None):
        if string[0] in meta or countbrackets(string) == False:
            print('Неправильно введено регулярное выражение')
            self.root = None            #здесь подправила, убрала флаг
            return
        string = ClearString(string)
        string = PrepareString(string, eclist)
        if len(string) > 3:
            string = copy(string)
            string = ClearString(string)            #тут добавила, заработало

        #print('Обрабатываемая подстрока: ', string)
        if currentnode == None:
            self.root = Node('root', None, None)
            currentnode = self.root
        else:
            currentnode = currentnode

        if currentnode == self.root and len(string) == 1:
            currentnode.val = string
        else:
            leftBegin = 0
            leftEnd = FindEnd(string)
            if string[leftEnd] in meta:
                if len(string) == leftEnd + 1:  # справа больше нет символов, при этом последний - мета (?,*)
                    currval = string[leftEnd]
                    currentnode.val = currval
                    currentnode.left = Node(ClearString(string[leftBegin: leftEnd]), None, None)
                    currentnode.right = None
                elif string[leftEnd] == '?' or string[leftEnd] == '*':
                    if string[leftEnd + 1] == '|':
                        currentnode.val = '|'
                    else:
                        currentnode.val = '.'
                    rightBegin = leftEnd + 1
                    rightEnd = len(string)
                    currentnode.left = Node(ClearString(string[leftBegin: leftEnd + 1]), None, None)
                    currentnode.right = Node(ClearString(string[rightBegin: rightEnd]), None, None)
                else:
                    currval = string[leftEnd]
                    rightBegin = leftEnd + 1
                    rightEnd = len(string)
            else:
                currval = '.'
                rightBegin = leftEnd
                rightEnd = len(string)

            if currentnode.left == None and currentnode.right == None:
                currentnode.val = currval
                currentnode.left = Node(ClearString(string[leftBegin: leftEnd]), None, None)
                currentnode.right = Node(ClearString(string[rightBegin: rightEnd]), None, None)

            if currentnode.left != None and len(currentnode.left.val) > 1:
                self.BuildTree(currentnode.left.val, currentnode.left)
            if currentnode.right != None and len(currentnode.right.val) > 1:
                self.BuildTree(currentnode.right.val, currentnode.right)

#tr = SyntaxTree()
#tr.BuildTree('a(bc)*')
#printTree(tr.root)
#reverseTree(tr.root)
##tr.BuildTree('s')            #+
##tr.BuildTree('((g|a|u{4}i)(L1){3}8){2}')           #+
##tr.BuildTree('a{3}*')           #+  (aaa)*
##tr.BuildTree('(a)*')            #+
##tr.BuildTree('((g|a|u{4}i)(L1){3}8){2}*')     #даже такое работает
#printTree(tr.root)
