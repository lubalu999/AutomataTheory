from SyntaxTree import *

import copy as cp

class GraphLink:  # Тип соединения в графе
    def __init__(self, link):
        self.link = link


class GraphNode:  # Нода графа
    def addlink(self, link, node):  # добавить переход и состояние (имя)
        self.links.append(link)
        self.nodes.append(node)

    def __init__(self, val=''):
        self.val = val  # номер состояния
        self.start = 0  # 1-стартовое
        self.end = 0  # 1-конечное
        self.links = []  # список переходов по символам
        self.nodes = []  # соотв. список состояний в которые попадаем по переходам (символам


class Auto:  # Класс автомата
    def __init__(self):
        self.Tree = SyntaxTree()
        self.GraphRoot = GraphNode()
        self.SymList = []  # without eps
        self.matrix = {}  # Матрица ДФА
        self.DFAmatrix = {}
        self.NewStates = {}
        self.GDFA = nx.MultiDiGraph()  # для визуализации
        self.GDFAedges = {}
        self.EmptyStateDFA = ''
        self.StartStateDFA = 0
        self.LastStatesDFA = []

        self.minDFAStatesFirst = {}
        self.MinDFAStart = 0
        self.MinDFAEnd = []
        self.GmDFA = nx.MultiDiGraph()  # для визуализации
        self.GmDFAedges = {}
        self.Groups = 2

    def BuildGraph(self, node):
        if node != None:
            self.BuildGraph(node.left)
            self.BuildGraph(node.right)
            if node.val not in meta:
                if node.val not in self.SymList:
                    self.SymList.append(node.val)
                self.Tree.Gedges, self.Tree.G, self.Tree.count, node.GraphRoot, node.GraphEnd = BuildNonMeta(
                    self.Tree.Gedges, self.Tree.G, self.Tree.count, node.val)
            if node.val == '|':
                self.Tree.Gedges, self.Tree.G, self.Tree.count, node.GraphRoot, node.GraphEnd = BuildOr(
                    self.Tree.Gedges, self.Tree.G, self.Tree.count, node.left.GraphRoot, node.right.GraphRoot,
                    node.left.GraphEnd, node.right.GraphEnd)
            if node.val == '.':
                self.Tree.Gedges, self.Tree.G, self.Tree.count, node.GraphRoot, node.GraphEnd = BuildAnd(
                    self.Tree.Gedges, self.Tree.G, self.Tree.count, node.left.GraphRoot, node.right.GraphRoot,
                    node.left.GraphEnd, node.right.GraphEnd)
            if node.val == '*':
                if node.left != None:
                    self.Tree.Gedges, self.Tree.G, self.Tree.count, node.GraphRoot, node.GraphEnd = BuildClini(
                        self.Tree.Gedges, self.Tree.G, self.Tree.count, node.left.GraphRoot, node.left.GraphEnd)
                else:
                    self.Tree.Gedges, self.Tree.G, self.Tree.count, node.GraphRoot, node.GraphEnd = BuildClini(
                        self.Tree.Gedges, self.Tree.G, self.Tree.count, node.right.GraphRoot, node.right.GraphEnd)
            if node.val == '?':
                if node.left != None:
                    self.Tree.Gedges, self.Tree.G, self.Tree.count, node.GraphRoot, node.GraphEnd = BuildOptional(
                        self.Tree.Gedges, self.Tree.G, self.Tree.count, node.left.GraphRoot, node.left.GraphEnd)
                else:
                    self.Tree.Gedges, self.Tree.G, self.Tree.count, node.GraphRoot, node.GraphEnd = BuildOptional(
                        self.Tree.Gedges, self.Tree.G, self.Tree.count, node.right.GraphRoot, node.right.GraphEnd)
            self.GraphRoot = node.GraphRoot
            self.GraphEnd = node.GraphEnd

    def CreateGraph(self):
        self.graph = {}
        for i in self.Tree.Gedges.keys():
            if i[0] not in self.graph.keys():
                self.graph[i[0]] = {i[1]: self.Tree.Gedges[i]}
            else:
                self.graph[i[0]][i[1]] = self.Tree.Gedges[i]
        self.graph[self.GraphEnd.val] = {}

    def RemoveShielding(self):
        for state in self.Tree.Gedges.keys():
            if self.Tree.Gedges[state] in reveclist.keys():
                self.SymList.remove(self.Tree.Gedges[state])
                self.Tree.Gedges[state] = reveclist[self.Tree.Gedges[state]]
                self.SymList.append(self.Tree.Gedges[state])

    def checkCycle(self, CurrState):
        flag = False
        for i in self.NewStates.keys():
            if self.NewStates[CurrState] == self.NewStates[i] and CurrState != i:
                return i
        return False

    def check(self, curr_state, graph):
        flag = False
        for k in list(graph.keys()):
            if k[0] == curr_state and 'eps' in graph[k]:
                flag = True
        return flag

    def DFA(self):
        begin = self.GraphRoot.val
        graph = self.Tree.Gedges
        new_states = []
        stack = [begin]
        first_states = [begin]
        counter = -1
        while len(stack) > 0:
            counter += 1
            #print('stack на шаге ' + str(counter) + '= ', stack)
            if len(stack) == 0:
                return new_states
            curr_state = stack.pop(-1)
            new_states.append([curr_state])
            first_states.append(curr_state)
            newmatrDFA = cp.copy(graph)
            while self.check(curr_state, newmatrDFA):  # В цикле удаляем все эпсидон переходы
                for i in list(newmatrDFA.keys()):
                    if i in list(newmatrDFA.keys()):
                        if i[0] == curr_state and newmatrDFA[i] == 'eps':
                            new_states[counter].append(i[1])
                            del newmatrDFA[i]
                            for j in list(newmatrDFA.keys()):
                                if j[0] == i[1]:
                                    prom = newmatrDFA[j]
                                    newmatrDFA[(curr_state, j[1])] = prom
                                    del newmatrDFA[j]
            for k in list(newmatrDFA.keys()):
                if k[0] == curr_state and newmatrDFA[k] != 'eps' and k[1] not in stack and k[1] != curr_state and k[
                    1] not in first_states:
                    stack.append(k[1])
        return new_states

    def AddEmpty(self):
        self.NodesCounter = len(self.listOfNewConst) - 1
        for i in list(self.NewStates.keys()):
            lstTrans = []
            if self.GraphEnd.val in self.NewStates[i]:
                self.LastStatesDFA.append(i)
            for p in list(self.GDFAedges.keys()):
                if p[0] == i:
                    lstTrans += self.GDFAedges[p]
            if lstTrans != self.SymList:
                for k in self.SymList:
                    if k not in lstTrans:
                        if self.NodesCounter + 1 not in self.NewStates.keys():
                            self.EmptyStateDFA = self.NodesCounter + 1
                            self.NewStates[self.NodesCounter + 1] = []
                            self.GDFAedges[(self.NodesCounter + 1, self.NodesCounter + 1)] = []
                            for j in self.SymList:
                                self.GDFAedges[(self.NodesCounter + 1, self.NodesCounter + 1)].append(j)
                        if (i, self.NodesCounter + 1) in self.GDFAedges.keys():
                            self.EmptyStateDFA = self.NodesCounter + 1
                            self.GDFAedges[(i, self.NodesCounter + 1)] += [k]
                        else:
                            self.EmptyStateDFA = self.NodesCounter + 1
                            self.GDFAedges[(i, self.NodesCounter + 1)] = [k]

    def rec_match(self, pos, state, string, flag):
        currState = state
        # print(pos, flag)
        if pos < len(string):
            for j in self.GDFAedges.keys():
                if ((string[pos] in self.GDFAedges[j]) and j[0] == currState):
                    # print('Переходим из вершины' + str(currState)+' в вершину '+ str(j[1]) + ' по ' + str(self.GDFAedges[j]), flag)
                    flag += self.rec_match(pos + 1, j[1], string, flag)
        else:
            return (currState in self.LastStatesDFA)
        return flag

    def FindAll(self, test_str):
        fndall = []
        res = [test_str[i: j] for i in range(len(test_str)) for j in range(i + 1, len(test_str) + 1)]
        for i in res:
            if self.rec_match(0, auto.StartStateDFA, i, False) > 0 and set(list(i)).issubset(set(self.SymList)):
                fndall.append(i)
        return fndall

    def BuildGraphDFA(self):  # (5,), (2, 6), (4, 6), ()
        self.NewStates = {}
        for y in range(len(self.listOfNewConst)):
            self.NewStates[y] = self.listOfNewConst[y]

        for group in range(len(self.listOfNewConst)):  # (13, 3, 14, 1, 4, 11, 9, 12, 5, 7, 3, 14)
            if self.GraphRoot.val in self.listOfNewConst[group]:
                self.StartStateDFA = group
            for state in self.listOfNewConst[group]:  # 13
                for est in self.Tree.Gedges.keys():  # (1, 2): 'a'
                    if est[0] == state and self.Tree.Gedges[est] != 'eps':  # есть переход по букве в est[1] либо в это же состояние ДКА, либо в другое. построим
                        for podgroup in range(len(self.listOfNewConst)):
                            if est[1] in self.listOfNewConst[podgroup]:
                                if (group, podgroup) not in self.GDFAedges:
                                    self.GDFAedges[(group, podgroup)] = []
                                self.GDFAedges[(group, podgroup)].append(self.Tree.Gedges[est])

    def MinDFA(self):
        lst_nodes = []  # хочу создать список с состояниями
        for i in self.newmatrDFA.keys():
            for j in i:
                if j not in lst_nodes:
                    lst_nodes.append(j)

        self.matrixMinDFA = [[''] * (len(lst_nodes) + 1) for i in
                             range(len(lst_nodes) + 1)]  # создадим двумерный массив состояний
        self.matrixMinDFA[0][0] = '№'

        for i in range(1, len(lst_nodes) + 1):  # U - Unmergered, ? - MightBeMergered
            self.matrixMinDFA[i][0] = lst_nodes[i - 1]
            for j in range(1, len(lst_nodes) + 1):
                if i == 1:
                    self.matrixMinDFA[0][j] = lst_nodes[j - 1]
                elif i <= j:
                    continue
                elif self.EmptyStateDFA == self.matrixMinDFA[i][0] or self.EmptyStateDFA == self.matrixMinDFA[0][j]:
                    self.matrixMinDFA[i][j] = 'U'
                elif i > j and (self.matrixMinDFA[i][0] not in self.LastStatesDFA and self.matrixMinDFA[0][
                    j] not in self.LastStatesDFA or
                                self.matrixMinDFA[i][0] in self.LastStatesDFA and self.matrixMinDFA[0][
                                    j] in self.LastStatesDFA):
                    self.matrixMinDFA[i][j] = '?'
                else:
                    self.matrixMinDFA[i][j] = 'U'

        #for s in self.matrixMinDFA:
        #    print(s)
        flag_finish = True
        while (flag_finish):
            flag_finish = False
            for i in range(1, len(lst_nodes) + 1):
                for j in range(1, len(lst_nodes) + 1):
                    if self.matrixMinDFA[i][j] == '?':  # нужно проверить, что переходы в классы эквивалентности
                        for sim in self.SymList:
                            sevsims1 = 0
                            sevsims2 = 0
                            sevsims11 = 0
                            sevsims22 = 0
                            for state in self.newmatrDFA.keys():
                                if self.matrixMinDFA[i][0] == state[0] and sim in self.newmatrDFA[state]:
                                    if state[1] in self.LastStatesDFA:
                                        sevsims1 +=1
                                    if state[1] not in self.LastStatesDFA:
                                        sevsims2 +=1
                                if self.matrixMinDFA[0][j] == state[0] and sim in self.newmatrDFA[state]:
                                    if state[1] in self.LastStatesDFA:
                                        sevsims11 += 1
                                    if state[1] not in self.LastStatesDFA:
                                        sevsims22 += 1
                            if not((sevsims1 > 0 and sevsims11 > 0) or (sevsims2 > 0 and sevsims22 > 0)):
                                self.matrixMinDFA[i][j] = 'U'
                                flag_finish = True
                                break


        #for s in self.matrixMinDFA:
        #    print(s)
        lst_new_nodes = []
        for i in range(1, len(lst_nodes) + 1):              #тут неверно
            for j in range(1, len(lst_nodes) + 1):
                if self.matrixMinDFA[i][j] == '?':
                    if lst_new_nodes == []:
                        lst = [self.matrixMinDFA[0][j], self.matrixMinDFA[i][0]]
                        lst_new_nodes.append(list(set(lst)))
                    else:
                        for states in range(len(lst_new_nodes)):
                            if self.matrixMinDFA[0][j] in lst_new_nodes[states] and self.matrixMinDFA[i][0] not in \
                                    lst_new_nodes[states]:
                                lst_new_nodes[states].append(self.matrixMinDFA[i][0])
                                lst_new_nodes[states] = list(set(lst_new_nodes[states]))
                                finish = True
                            elif self.matrixMinDFA[i][0] in lst_new_nodes[states] and self.matrixMinDFA[0][j] not in \
                                    lst_new_nodes[states]:
                                lst_new_nodes[states].append(self.matrixMinDFA[0][j])
                                lst_new_nodes[states] = list(set(lst_new_nodes[states]))
                                finish = True
                            elif self.matrixMinDFA[i][0] not in lst_new_nodes and self.matrixMinDFA[0][j] not in lst_new_nodes:
                                lst = [self.matrixMinDFA[0][j], self.matrixMinDFA[i][0]]
                                lst_new_nodes.append(list(set(lst)))

        temp = []
        for x in lst_new_nodes:
            if x not in temp:
                add = True
                for u in temp:
                    if set(x).issubset(u):
                        add = False
                if add == True:
                    temp.append(x)

        lst_new_nodes = temp
        for i in lst_nodes:
            fladd = True
            for j in range(len(lst_new_nodes)):
                if i in lst_new_nodes[j]:
                    fladd = False
                    break
            if fladd == True:
                lst_new_nodes.append([i])

        # сделаем переходы               [[1, 2, 3], [0], [7]]
        for i in range(len(lst_new_nodes)):  # [1, 2, 3]
            for j in lst_new_nodes[i]:  # 1
                if j in self.LastStatesDFA and i not in self.MinDFAEnd:
                    self.MinDFAEnd.append(i)
                if j == self.StartStateDFA:
                    self.MinDFAStart = i
                for state in self.newmatrDFA:  # (0,1), (2,3), ...
                    if j == state[0]:
                        for group in range(len(lst_new_nodes)):  # oпределим в какую группу добавлять переход
                            if state[1] in lst_new_nodes[group]:
                                if (i, group) not in self.GmDFAedges:
                                    self.GmDFAedges[(i, group)] = []
                                    #self.GmDFAedges[(i, group)].append(self.newmatrDFA[state])
                                #else:
                                    # могут случится дубликаты, уберём их
                                for sim in self.newmatrDFA[state]:  # ['a','b']
                                    if sim not in self.GmDFAedges[(i, group)]:
                                        self.GmDFAedges[(i, group)].append(sim)
        print("self.GmDFAedges",self.GmDFAedges)
        print("StartMinDFA =",self.MinDFAStart, "EndMinDFA =",self.MinDFAEnd)

    def KPath(self, start, finish, kpath):
        lst_nodes = self.GmDFA.nodes()
        R = {}
        k = -1
        n = len(lst_nodes)

        for i in range(len(lst_nodes)):  # -1 step, базис
            for j in range(len(lst_nodes)):
                R[i, j] = {k: ''}
                if i == j:
                    R[i, j][k] += 'eps'
                if (i, j) in self.GmDFAedges:
                    for sim in self.GmDFAedges[(i, j)]:
                        if R[i, j][k] == '':
                            R[i, j][k] += sim
                        else:
                            R[i, j][k] += '|' + sim
                if R[i, j][k] == '':
                    R[i, j][k] += '∅'


        k += 1

        while k < n:
            for i in range(len(lst_nodes)):  # 0, 1, 2... step
                for j in range(len(lst_nodes)):  #
                    if (R[i, k][k - 1] == '∅' or R[k, k][k - 1] == '∅' or R[k, j][k - 1] == '∅') and R[i, j][k - 1] == '∅':
                        R[i, j][k] = '∅'
                    elif R[i, k][k - 1] == '∅' or R[k, k][k - 1] == '∅' or R[k, j][k - 1] == '∅':
                        R[i, j][k] = R[i, j][k - 1]
                    elif R[i, j][k - 1] == '∅':
                        R[i, j][k] = '('+R[i, k][k - 1]+ ')' + '(' + R[k, k][k - 1] + ')*' +'('+ R[k, j][k - 1]+ ')'
                    else:
                        if R[i, j][k - 1] in R[i, k][k - 1] or R[i, j][k - 1] in R[k, k][k - 1] or R[i, j][k - 1] in R[k, j][k - 1]:
                            R[i, j][k] = '(' + R[i, k][k - 1]+ ')' + '(' + R[k, k][k - 1] + ')*' +'(' + R[k, j][k - 1]+ ')' + '|' + '(' + R[i, j][k - 1] + ')'
                        else:
                            R[i, j][k] =  '(' + R[i, k][k - 1]+ ')' + '(' + R[k, k][k - 1] + ')*' +'(' + R[k, j][k - 1] + ')'+ '|' + '(' + R[i, j][k - 1] + ')'

            k += 1


        #сделаем экранирование, если оно было
        R[start, finish][kpath] = R[start, finish][kpath].replace('**', '*%*%')
        R[start, finish][kpath] = R[start, finish][kpath].replace('|*', '|%*%')
        R[start, finish][kpath] = R[start, finish][kpath].replace('?', '%?%')
        R[start, finish][kpath] = R[start, finish][kpath].replace('*|', '*%|%')
        R[start, finish][kpath] = R[start, finish][kpath].replace('||', '|%|%')
        R[start, finish][kpath] = R[start, finish][kpath].replace('.', '%.%')
        R[start, finish][kpath] = R[start, finish][kpath].replace('eps|', '|')
        R[start, finish][kpath] = R[start, finish][kpath].replace('|eps', '|')
        R[start, finish][kpath] = R[start, finish][kpath].replace('(|', '(')
        R[start, finish][kpath] = R[start, finish][kpath].replace('|)', ')')
        R[start, finish][kpath] = R[start, finish][kpath].replace('eps', '')
        R[start, finish][kpath] = R[start, finish][kpath].replace('()*', '')
        R[start, finish][kpath] = R[start, finish][kpath].replace('()', '')

        return R[start, finish][kpath]

    def Inversion(self):
        self.InvDFA = {}
        self.InvStartes = self.LastStatesDFA
        self.InvEnd = self.StartStateDFA

        for i,j in self.GDFAedges.keys():
            self.InvDFA[j,i] = self.GDFAedges[i,j]

        dict = {}                           #теперь нужно создать новое стартовое состояние и по ЕПС-переходам совместить со стартовыми Инвертированного ДКА
        for k in self.InvDFA.keys():
            if k[0] in self.InvStartes:
                dict[self.NodesCounter+2,k[0]] = 'eps'
        for key in dict.keys():
            self.InvDFA[key] = dict[key]


        self.InvStartes = self.NodesCounter+2
        self.GraphRoot.val = self.InvStartes
        self.Tree.Gedges = self.InvDFA
        lst_temp = {}
        self.listOfNewConst = self.DFA()            #Новый ДКА

        for group in range(len(self.listOfNewConst)):
            for state in self.listOfNewConst[group]:  # 4
                for est in self.InvDFA.keys():  # (1, 2): 'a'
                    if est[0] == state and self.Tree.Gedges[est] != 'eps':
                        for podgroup in range(len(self.listOfNewConst)):
                            if est[1] in self.listOfNewConst[podgroup]:
                                if (group, podgroup) not in lst_temp:
                                    lst_temp[(group, podgroup)] = []
                                for sim in self.Tree.Gedges[est]:
                                    if sim not in lst_temp[(group, podgroup)]:
                                        lst_temp[(group, podgroup)].append(sim)


        self.InvDFA = lst_temp
        self.DFAG = nx.DiGraph()
        for i in range(len(self.listOfNewConst)):
            if self.GraphRoot.val in self.listOfNewConst[i]:
                self.StartStateDFA = i
            if self.GraphEnd.val in self.listOfNewConst[i]:
                self.LastStatesDFA = i
        print("StartStateDFAInversion", self.StartStateDFA)
        print("LastStatesDFAInversion", self.LastStatesDFA)

        self.DFAG.add_edges_from(self.InvDFA)
        pos = nx.spring_layout(self.DFAG)
        nx.draw(self.DFAG, with_labels=True, pos=pos)
        nx.draw_networkx_edge_labels(
            self.DFAG, pos,
            edge_labels=self.InvDFA,
            font_color='red'
        )
        plt.show()


    def AutoCompile(self, regexp):
        # Строим дерево
        self.Tree = SyntaxTree()
        self.Tree.BuildTree(regexp)
        printTree(self.Tree.root)
        # Строим НКА
        self.BuildGraph(self.Tree.root)
        self.CreateGraph()
        self.RemoveShielding()
        pos = nx.spring_layout(self.Tree.G)
        nx.draw(self.Tree.G, with_labels=True, pos = pos)
        nx.draw_networkx_edge_labels(
            self.Tree.G, pos,
            edge_labels = self.Tree.Gedges,
            font_color='red'
        )
        plt.show()
        # Строим ДКА
        #print(self.GraphRoot.val)
        self.listOfNewConst = self.DFA()

        self.BuildGraphDFA()
        self.AddEmpty()
        self.newmatrDFA = self.GDFAedges
        self.DFAG = nx.DiGraph()
        print("StartStateDFA",self.StartStateDFA)
        print("LastStatesDFA",self.LastStatesDFA)
        #print(self.GDFAedges)
        self.DFAG.add_edges_from(self.GDFAedges)
        pos = nx.spring_layout(self.DFAG)
        nx.draw(self.DFAG, with_labels=True, pos = pos)
        nx.draw_networkx_edge_labels(
            self.DFAG, pos,
            edge_labels = self.GDFAedges,
            font_color='green'
        )
        plt.show()

        self.MinDFA()
        self.GmDFA = nx.DiGraph()
        self.GmDFA.add_edges_from(self.GmDFAedges)
        pos = nx.spring_layout(self.GmDFA)
        nx.draw(self.GmDFA, with_labels=True, pos=pos)
        nx.draw_networkx_edge_labels(
            self.GmDFA, pos,
            edge_labels=self.GmDFAedges,
            font_color='orange'
        )
        plt.show()

        #print("Инвертируем ДКА:")
        #self.Inversion()
        print("Восстановление регулярного выражения методом К-пути",self.KPath(1, 0, 2))

def mul(a1,a2):
    res = {}
    nodes = list(nx.cartesian_product(a1.DFAG, a2.DFAG).nodes())
    for node1 in nodes:
        for node2 in nodes:
            if (node1[0], node2[0]) in list(a1.newmatrDFA.keys()) and (node1[1], node2[1]) in list(a2.newmatrDFA.keys()):
                if len(set(a1.newmatrDFA[(node1[0], node2[0])]).intersection(set(a2.newmatrDFA[(node1[1], node2[1])])))>0:
                    res[(node1, node2)] = list(set(a1.newmatrDFA[(node1[0], node2[0])]).intersection(set(a2.newmatrDFA[(node1[1], node2[1])])))
    return res


def FindWay(node, val):
    listNodes = []  # Список номеров нод в которые мы приходим из текущей по val
    for i in range(len(node.links)):
        if node.links[i] == val and node.nodes[i].val not in listNodes:
            listNodes.append(node.nodes[i].val)
        if node.links[i] == 'eps' and node.nodes[i].val not in listNodes:
            listNodes = listNodes + FindWay(node.nodes[i], val)
    return listNodes


def BuildClini(edges, G, count, leftroot, leftend):
    count += 1
    root = GraphNode(count)
    root.start = 1

    leftroot.start = 0
    root.addlink('eps', leftroot)
    G.add_edge(root.val, leftroot.val)
    edges[(root.val, leftroot.val)] = 'eps'
    count += 1
    end = GraphNode(count)
    end.end = 1
    leftend.end = 0
    leftend.addlink('eps', leftroot)
    G.add_edge(leftend.val, leftroot.val)
    edges[(leftend.val, leftroot.val)] = 'eps'
    leftend.addlink('eps', end)
    G.add_edge(leftend.val, end.val)
    edges[(leftend.val, end.val)] = 'eps'
    root.addlink('eps', end)
    G.add_edge(root.val, end.val)
    edges[(root.val, end.val)] = 'eps'
    return edges, G, count, root, end


def BuildOptional(edges, G, count, leftroot, leftend):
    count += 1
    root = GraphNode(count)
    root.start = 1

    leftroot.start = 0
    root.addlink('eps', leftroot)
    G.add_edge(root.val, leftroot.val)
    edges[(root.val, leftroot.val)] = 'eps'

    count += 1
    end = GraphNode(count)
    end.end = 1

    leftend.end = 0
    leftend.addlink('eps', end)
    G.add_edge(leftend.val, end.val)
    edges[(leftend.val, end.val)] = 'eps'
    root.addlink('eps', end)
    G.add_edge(root.val, end.val)
    edges[(root.val, end.val)] = 'eps'
    return edges, G, count, root, end


def BuildAnd(edges, G, count, leftroot, rightroot, leftend, rightend):
    root = leftroot
    root.start = 1
    end = rightend
    end.end = 1

    leftend.end = 0
    rightroot.start = 0
    leftend.addlink('eps', rightroot)  # конец левого с началом правого
    G.add_edge(leftend.val, rightroot.val)
    edges[(leftend.val, rightroot.val)] = 'eps'
    return edges, G, count, root, end


def BuildNonMeta(edges, G, count, val):
    count += 1
    root = GraphNode(count)
    root.start = 1  # start state
    count += 1
    end = GraphNode(count)
    end.end = 1  # end state
    root.addlink(link=val, node=end)
    G.add_edge(root.val, end.val)  # передаем 2 номера состояний
    edges[(root.val, end.val)] = val  # (1,2): eps, например. 1,2 - номера состояний
    return edges, G, count, root, end


def BuildOr(edges, G, count, leftroot, rightroot, leftend, rightend):
    count += 1
    root = GraphNode(count)
    root.start = 1  # start state
    count += 1
    end = GraphNode(count)
    end.end = 1  # end state

    leftroot.start = 0  # больше не стартовое
    root.addlink('eps', leftroot)  # склеиваем новое стартовое состояние с левым подкорнем
    G.add_edge(root.val, leftroot.val)
    edges[(root.val, leftroot.val)] = 'eps'  # добавляем ребро в список (2,3): а...

    rightroot.start = 0  # больше не стартовое
    root.addlink('eps', rightroot)  # соединение по эпсилон старт. с правым начальным состоятием
    G.add_edge(root.val, rightroot.val)
    edges[(root.val, rightroot.val)] = 'eps'

    leftend.end = 0  # больше не конечное
    leftend.addlink('eps', end)  # сводим концы с концами
    G.add_edge(leftend.val, end.val)
    edges[(leftend.val, end.val)] = 'eps'

    rightend.end = 0  # больше не конечное
    rightend.addlink('eps', end)  # переход по эпсилон в конец
    G.add_edge(rightend.val, end.val)
    edges[(rightend.val, end.val)] = 'eps'
    return edges, G, count, root, end


auto = Auto()
auto.AutoCompile('abc')
auto1 = Auto()
auto1.AutoCompile('abc')
print(auto.FindAll('ab'))

res = mul(auto, auto1)
gr = nx.DiGraph()
gr.add_edges_from(res)
pos = nx.circular_layout(gr)
nx.draw(gr, with_labels=True, pos = pos)
nx.draw_networkx_edge_labels(
    gr, pos,
    edge_labels = res,
    font_color='purple'
)
plt.show()
