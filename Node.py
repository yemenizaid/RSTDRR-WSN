
class Node:
    def __init__(self):
        self.Node_id=0
        self.Coord=[]
        self.Neighbors=[]
        self.SensingRadius=0
        self.Hop2Intersectwith=[]
        self.data=[]
        self.next=None

    def setNext(self, node):
        self.next=node

    def getNext(self):
        return self.next

    def setNodeId(self, node_id):
        self.node_id=node_id

    def getNodeId(self):
        return self.node_id

    def setCoord(self, coord):
        self.Coord=coord

    def getCoord(self):
        return self.Coord

    def setRadius(self, radius):
        self.SensingRadius=radius

    def getRadius(self):
        return self.SensingRadius

    def setNeighbors(self, neighbors):
        self.Neighbors=neighbors

    def getNeighbors(self):
        return self.Neighbors

    def setSensorReading(self, data):
        self.data=data

    def getSensorReading(self):
        return self.data
    def insertNeighbor(self, node_id):
        self.Neighbors.append(node_id)
    def removeNode(self, node_id):
        self.Neighbors.remove(node_id)
