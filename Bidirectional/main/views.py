from django.shortcuts import render
from django.views import generic
from random import sample, randint, randrange
from django.views.decorators.csrf import csrf_exempt

import sys
import pdb


class Indexed(generic.TemplateView):
    template_name = 'main/index.html'


class Noded:
    cx = None
    cy = None
    relevant = set()
    StartFlag = False
    EndFlag = False
    iteration = 0
    used_X_cordinates = {0}
    used_Y_cordinates = {0}
    checked = False

    #   returns random number for Circle and removing unusable (too close) X parameters
    def getCX(self, request):
        X_set = set(range(10, int(request.POST['TheWidth']) - 5))
        cx = sample((X_set - self.used_X_cordinates), 1)
        self.used_X_cordinates.update(set(range(abs(cx[0] - 5), cx[0] + 5)))
        return cx[0]

    #   returns random number for Circle and removing unusable (too close) Y parameters
    def getCY(self, request):
        Y_set = set(range(10, int(request.POST['TheHeight']) - 5))
        cy = sample((Y_set - self.used_Y_cordinates), 1)
        self.used_Y_cordinates.update(set(range(abs(cy[0] - 5), cy[0] + 5)))
        return cy[0]

    # def __str__(self):
    #     return str(self.cx)


class GetMyPost(generic.TemplateView):
    template_name = 'main/gotthepost.html'

    def __init__(self):
        super().__init__()
        self.GetTheFlag = True
        self.count = 0
        self.availables = set()

    def post(self, request):
        self.Nodes = []
        Noded.used_X_cordinates = {0}
        Noded.used_Y_cordinates = {0}
        #       receiving the number of Nodes from User
        my_data = request.POST['post_form']

        #       initializing The inner Width and Height of the Screen
        TheWidth = request.POST['TheWidth']
        BFS.TheWidth = request.POST['TheWidth']
        BFS.TheHeight = request.POST['TheHeight']
        TheHeight = request.POST['TheHeight']

        for i in range(0, int(my_data)):
            Node = Noded()
            Node.cx = Node.getCX(request=request)
            Node.cy = Node.getCY(request=request)
            Node.getCY(request=request)
            self.Nodes.append(Node)
            Node.relevant = set()

        print("mmm", " ", len(self.Nodes), "  ",  "mmmm")
        self.availables = set()
        self.availables.update(self.Nodes)
        # self.NodeRel(self.availables.copy())

        # self.RelevantHandler(self.availables)
        # while self.GetTheFlag:
        #     self.availables = set()
        #     self.availables.update(self.Nodes)
        #     self.count += 1
        #     if self.count > 1000:
        #         assert 0, "Recursive boooy 1000"
        #     self.NodeRel(self.availables.copy())

        while self.GetTheFlag:
            self.NodeRel(self.availables.copy())
            self.availables = set()
            self.availables.update(self.Nodes)
            for NODE in self.Nodes:
                NODE.checked = False

        self.EdgeCalculation()

        BFS.Nodes = self.Nodes
        BFS.edgeList = self.edgeList

        # assert 0
        context = {'Nodes': self.Nodes, 'TheWidth': TheWidth, 'TheHeight': TheHeight, 'edgeList': self.edgeList}
        return render(request, self.template_name, context=context)

    # def RelevantHandler(self, availables):
    #
    #     for Node in availables:
    #         availables.remove(Node)
    #         to_choose_from = (set(availables) - set(Node.relevant))
    #
    #         if len(Node.relevant) > 0:
    #             chosen = sample(to_choose_from, 1)
    #         else:
    #             chosen = sample(to_choose_from, 1)
    #
    #         for item in chosen:
    #             item.relevant.add(Node)
    #             Node.relevant.add(item)
    #         if len(to_choose_from) > 1:
    #             availables.append(Node)

    def NodeRel(self, CurAvailables):
        for Node in CurAvailables:
            if Node in self.availables:
                self.availables.remove(Node)

            if len(Node.relevant) == 0:
                chosen = sample(CurAvailables, randint(1, 2 - len(Node.relevant)))

            elif 3 > len(Node.relevant) > 0:
                chosen = sample(CurAvailables, randint(0, 2 - len(Node.relevant)))

            else:
                continue

            for item in chosen:
                item.relevant.add(Node)
                Node.relevant.add(item)
                if len(item.relevant) > 1 and item in self.availables:
                    self.availables.remove(item)

        # sys.setrecursionlimit(100)
        test = set()

        def tester(Nody):
            test.add(Nody)
            Nody.checked = True
            for relly in Nody.relevant:
                if not relly.checked:
                    test.add(relly)
                    relly.checked = True
                    tester(relly)
                if relly.checked:
                    test.add(relly)

        tester(self.Nodes[0])
        print("\n\n\n\n")
        print(len(test), "\t", len(self.availables), len(self.Nodes))
        print("\n\n\n\n")
        if len(test) != len(self.Nodes):
            self.GetTheFlag = True

        elif len(test) == len(self.Nodes):
            self.GetTheFlag = False
            # pdb.set_trace()
            # CurAvailables = set()
            # chosen = None
            # self.availables = set()
            # self.availables.update(self.Nodes)
            # self.NodeRel(self.Nodes)

    def EdgeCalculation(self):
        self.edgeList = []
        for Node in self.Nodes:
            for item in Node.relevant:
                if (Node, item) and (item, Node) not in self.edgeList:
                    self.edgeList.append((Node, item))
                    self.edgeList.append((item, Node))

        del self.edgeList[1::2]


class BFS(generic.TemplateView):
    template_name = 'main/bfs.html'

    def __init__(self):
        super().__init__()

    # sys.setrecursionlimit(5500)
    TheFlag = True
    ReachNode = None
    StartNodeQuery = set()
    EndNodeQuery = set()
    index = 1
    TheWidth = None
    TheHeight = None
    Nodes = []
    edgeList = []
    Start_Node = None
    End_Node = None

    def GetTheStartNode(self, x, y):
        for Node in self.Nodes:
            if Node.cx == x and Node.cy == y:
                self.Start_Node = Node
                self.StartNodeQuery.add(self.Start_Node)

    def GetTheEndNode(self, x, y):
        for Node in self.Nodes:
            if Node.cx == x and Node.cy == y:
                self.End_Node = Node
                self.EndNodeQuery.add(self.End_Node)

    def iterator(self, CurrentStartQuery, CurrentEndQuery):
        # pdb.set_trace()

        for Node in self.Nodes:
            if len(Node.relevant) < 1:
                assert 0

        for Node in CurrentStartQuery:
            if not Node.EndFlag:
                # it hasn't been checked
                if not Node.StartFlag:
                    for item in Node.relevant:
                        if item.iteration == 0:
                            item.iteration = self.index + 1
                            # item.StartFlag = True
                    self.StartNodeQuery.update(Node.relevant)
                    Node.StartFlag = True
                    Node.iteration = self.index

                # it already has been checked
                # else:
                #     continue
            # End Flag Was True, They Reached Each other
            elif self.ReachNode is None:
                Node.StartFlag = None
                Node.EndFlag = None
                # Node.iteration = index   probably bad
                self.ReachNode = Node
                # self.TheFlag = False
                # break

        if self.ReachNode is None:
            for Node2 in CurrentEndQuery:
                if not Node2.StartFlag:
                    # it hasn't been checked
                    if not Node2.EndFlag:
                        for item in Node2.relevant:
                            if item.iteration == 0:
                                item.iteration = self.index + 1
                                # item.EndFlag = True
                        self.EndNodeQuery.update(Node2.relevant)
                        Node2.EndFlag = True
                        Node2.iteration = self.index
                    # it already has been checked
                    # else:
                    #     continue
                # Start Flag Was True, They Reached Each other
                elif self.ReachNode is None:
                    Node2.EndFlag = None
                    Node2.StartFlag = None
                    # Node2.iteration = index2  probably bad
                    self.ReachNode = Node2
                    # self.TheFlag = False
                    # break

        if self.ReachNode is not None:
            self.TheFlag = False

        self.index += 1

    def post(self, request):
        self.TheFlag = True
        self.ReachNode = None
        self.StartNodeQuery = set()
        self.EndNodeQuery = set()
        self.index = 1
        self.Start_Node = None
        self.End_Node = None
        count = 1

        self.GetTheStartNode(int(request.POST['Node1X']), int(request.POST['Node1Y']))
        self.GetTheEndNode(int(request.POST['Node2X']), int(request.POST['Node2Y']))

        while self.TheFlag:
            # count += 1
            # if count > 1000:
            #     return render(request, 'main/index.html')
            SNQ = self.StartNodeQuery
            ENQ = self.EndNodeQuery
            self.iterator(SNQ.copy(), ENQ.copy())

        # for item in self.StartNodeQuery.copy():
        #     if item.iteration > self.ReachNode.iteration:
        #         self.StartNodeQuery.remove(item)

        context = {
            'Start_Node': self.Start_Node,
            'End_Node': self.End_Node,
            'ReachNode': self.ReachNode,
            'Nodes': self.Nodes,
            'edgeList': self.edgeList,
            'TheWidth': self.TheWidth,
            'TheHeight': self.TheHeight
            # 'StartNodeQuery': self.StartNodeQuery,
            # 'EndNodeQuery': self.EndNodeQuery
        }

        return render(request, 'main/bfs.html', context=context)
