from DataUpload import uploadData
from LinkedListStruct import LinkedList
import sys

from copy import deepcopy
import math

class Sink:
    def __init__(self, fname):
        self.fname=fname
        self.lls = LinkedList()
        self.lls = uploadData(fname)
        #self.ll=deepcopy(self.lls)

    def buildGroup(self):

        sortedlist=Sink.sortList(self)
        newlist=LinkedList()

        queue=[]

        for e in sortedlist:
            node_id=e[0]
            node=self.lls.findNode(node_id)
            if node.getNodeId() not in queue:
                newlist.addNode(deepcopy(node))
                for e in node.getNeighbors():
                    if e not in queue:
                        queue.append(e)
        #newlist.printLinkedList()
        self.lls=newlist

    def sortList(self):
        temp = self.lls.head
        list = []
        temp1 = None
        while temp is not None:
            list.append((temp.getNodeId(), len(temp.getNeighbors())))
            temp = temp.next
        for i in range(0, len(list) - 1):
            for j in range(i + 1, len(list)):
                if list[i][1] <= list[j][1]:
                    temp1 = list[i]
                    list[i] = list[j]
                    list[j] = temp1
        #print(list)
        return list

    def findNodeWithLargestNieghbors(self):
        numofnodes = 0
        node = None
        head = self.lls.head
        numofnodes = len(head.getNeighbors())
        node = self.lls.head
        temp = self.lls.head.next
        while temp is not None:
            if len(temp.getNeighbors()) <= numofnodes:
                numofnodes = len(temp.getNeighbors())
                node = temp
            temp = temp.next

        return node

    def findNodeWithSmallestNieghbors(self):
        return

    def findContainment(self):
        temp1 = self.lls.head
        newlls = LinkedList()
        containedFlag = False
        newnode = None

        while temp1 is not None:
            temp2 = temp1.next
            while temp2 is not None:
                if Sink.isContained(self, temp1.getNeighbors(), temp2.getNeighbors()):
                    if len(temp1.getNeighbors()) > len(temp2.getNeighbors()):
                        newnode = temp1
                        newnode.insertNeighbor(temp2.getNodeId())
                    elif len(temp2.getNeighbors()) > len(temp1.getNeighbors()):
                        newnode = temp2
                        newnode.insertNeighbor(temp1.getNodeId())
                    else:
                        newnode = temp2
                        newnode.insertNeighbor(temp1.getNodeId())
                    containedFlag = True
                temp2 = temp2.next
            if containedFlag:
                if not Sink.isInList(self, newnode.getNodeId(), newlls):
                    newlls.addNode(deepcopy(newnode))
                containedFlag = False
            else:
                if not Sink.isInList(self, temp1.getNodeId(), newlls):
                    newlls.addNode(deepcopy(temp1))
            temp1 = temp1.next
            newnode = None
        #newlls.printLinkedList()
        self.lls = newlls
        return newlls

    def isInList(self, node_id, newlls):
        temp1 = newlls.head
        while temp1 is not None:
            if temp1.getNodeId() == node_id:
                return True

            temp1 = temp1.next
        return False

    def isContained(self, a, b):
        if len(a) > len(b):
            for e in b:
                if e not in a:
                    return False
        elif len(b) > len(a):
            for e in a:
                if e not in b:
                    return False

        else:
            for e in a:
                if e not in b:
                    return False
        return True
    def findNearestGroup(self, group_1, group_2, node):
        if group_1 is None:
            return group_2

        if group_2 is None:
            return group_1

        dist_1 = Sink.findDistance(self,group_1.getCoord(), node.getCoord())
        dist_2 = Sink.findDistance(self,group_2.getCoord(), node.getCoord())
        #print("hghgh", dist_1, "  ", dist_2, node.getNodeId())
        if dist_1 <= dist_2:
            return group_1

        return group_2
    def findDistance(self, node_1, node_2):
        x1 = node_1[0]
        x2 = node_2[0]
        y1 = node_1[1]
        y2 = node_2[1]
        dist = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
        return dist

    def refineGroups(self):
        temp1=self.lls.head
        ll = LinkedList()
        ll = uploadData(self.fname)
        #self.lls.printLinkedList()
        while temp1 is not None:
            temp2 = temp1.next
            #print("temp1", temp1.Neighbors)
            while temp2 is not None:
                #print("temp2", temp2.Neighbors)
                for el in temp1.Neighbors:

                    if el in temp2.Neighbors:
                        #print("el",el)
                        node=ll.findNode(el)
                        group=Sink.findNearestGroup(self,temp1, temp2, node)
                        if group.getNodeId() == temp1.getNodeId():
                            temp2.removeNode(el)
                            self.lls.updateNode(temp2)
                        else:
                            temp1.removeNode(el)
                            self.lls.updateNode(temp1)
                temp2=temp2.next
            temp1=temp1.next
        #self.lls.printLinkedList()


sys.setrecursionlimit(10000)

"""s = Sink("wsns/200.txt")
s.lls.printLinkedList()
# node=s.findNodeWithLargestNieghbors()
# print(node.getNodeId(), "  ", node.getNeighbors())
#s.findContainment()
print(s.sortList())
s.buildGroup()
s.refineGroups()

s.lls.printLinkedList()"""
