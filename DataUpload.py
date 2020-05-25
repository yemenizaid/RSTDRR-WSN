from Node import Node
from LinkedListStruct import LinkedList

readSize = 500
smallestsize = 0


def uploadData(file_name):
    lls = LinkedList()
    try:
        f = open(file_name, 'r')
        while True:
            readline = f.readline()
            if readline == '' or len(readline) == 1:
                break
            lls.addNode(formulateData(readline))
    except IOError as e:
        print(" file cann't be found or open")
    return lls


def formulateData(readline):
    datalist = []
    node = Node()
    datalist = readline.split("|")
    datalist = datalist[0:len(datalist) - 1]
    # print(datalist)
    node.setNodeId(int(datalist[1].split(":")[1]))
    node.setCoord([float(datalist[2].split(":")[1])] + [float(datalist[3].split(":")[1])])
    node.setRadius(50)  # in meters
    for nghbr in datalist[4:]:

        if "Neighbors" in nghbr:
            if int(nghbr.split(":")[1]) == 0:
                continue
            node.Neighbors = node.Neighbors + [int(nghbr.split(":")[1])]
        else:
            if int(nghbr) == 0:
                continue
            node.Neighbors = node.Neighbors + [int(nghbr)]
    node.setSensorReading(readData(node.getNodeId()))
    return node


def readData(node_id):
    readingList = []
    count = 0
    global smallestsize
    try:
        f = open("datasets/Sensor_" + str(node_id) + ".txt", 'r')
        while True:
            readline = f.readline()
            if readline == '':
                break
            count += 1
            if count > readSize:
                break

            if " " not in readline:
                readingList.append(float(readline))
    except IOError as e:
        print(" file cann't be found or open")
    # readingList=refineData(readingList)
    if smallestsize > len(readingList):
        smallestsize = len(readingList)

    return readingList


def findsmallest(self, wsn):
    temp = len(wsn[0].data)
    for i in range(1, len(wsn)):
        if temp > len(wsn[i].data):
            temp = len(wsn[i].data)
    return temp


