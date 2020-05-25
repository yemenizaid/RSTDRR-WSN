import Node

class LinkedList:

    def __init__(self):
        self.head=None
        self.next=None
        self.tail=None

    '''
        add node to the end of the list.
        @param: node, it is an instance of Node class to be added to . 
    '''
    def addNode(self, node):

        if self.head==None:
            self.head=node
            self.tail=self.head
            self.head.next=None
        else:
            self.tail.next=node
            self.tail=self.tail.next
            self.tail.next=None

    '''
        search for a node in linkedlist by its id.
        @param: node_id, it is ID of the node to be searched. 
    '''
    def findNode(self, node_id):
        tempNode=self.head

        while(tempNode is not None):
            #print(tempNode.getNodeId())
            if int(tempNode.getNodeId())==int(node_id):
                return tempNode

            tempNode=tempNode.next
        return None

    '''
        update the node details such as coordinates and neighbors and 2hop neighbor nodes.
        @param: node, t is an instance of Node class used to update the node in the linkedlist. 
    '''
    def updateNode(self, node):
        tempNode=self.head

        while(tempNode is not None):
            if(tempNode.node_id==node.node_id):
                tempNode.Coord=node.Coord
                tempNode.Neighbors=node.Neighbors
                #tempNode.Hop2Intersectwith=node.Hop2Intersectwith
                return

            tempNode=tempNode.next


    def printLinkedList(self):
        tempNode=self.head

        while(tempNode is not None):
            print("node id:",tempNode.node_id)
            #print("Coords:", tempNode.Coord)
            print("Neighbors:", tempNode.Neighbors)
            tempNode=tempNode.next





