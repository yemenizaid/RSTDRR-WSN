from DataUpload import uploadData, readData
from Sink import Sink
import math

def round_up( n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

class sensor:
    def __init__(self, datasize):
        self.pattern=[]
        self.dataSize=datasize
        self.readings=[]
        self.lastPattern=0
        self.batCap = 3.6
        self.V = 3.6
        self.Itx = ((17.4 + 18.8 + 0.5 + 0.426) / 32768)
        self.totaltrans=0
        self.totalaggregationOutput = []


    def setPattern(self, pattern):
        self.pattern=pattern


    def findEnergyConsumption(self):

        #charge= self.Itx*(0.426+15)/32768
        charge=17.4/32768
        Etx = self.V * charge
        self.batCap=self.batCap-Etx
        #print(Etx*100, "  ", self.batCap)
        #print("for one message",Etx)

    def uploadData(self, sensor_id):
        readingList = []
        count = 0
        global smallestsize

        try:
            f = open("datasets/Sensor_" + str(sensor_id) + ".txt", 'r')
            while True:
                readline = f.readline()
                if readline == '':
                    break
                count += 1

                if count > self.dataSize:
                    break

                if " " not in readline:
                    self.readings.append(float(readline))
        except IOError as e:
            print(" file cann't be found or open")
        # readingList=refineData(readingList)

    def getNextReading(self, index):
        if self.lastPattern==0:
            for ind in range(1, len(self.pattern)):
                if round_up(self.readings[index]) >= self.pattern[ind][0] and round_up(self.readings[index]) <= self.pattern[ind][1]:
                    self.lastPattern=ind
                    sensor.findEnergyConsumption(self)
                    self.totaltrans +=1
                    return self.readings[index]
        else:
            for ind in range(1, len(self.pattern)):
                if round_up(self.readings[index])>=self.pattern[ind][0] and round_up(self.readings[index])<=self.pattern[ind][1]:
                    if ind ==self.lastPattern:
                        self.lastPattern=ind
                        return None
                    else:
                        self.lastPattern=ind
                        sensor.findEnergyConsumption(self)
                        self.totaltrans += 1
                        return self.readings[index]
actual_mean=0
actual_counter=0
energy_con=0
class ClusterHead:
    def __init__(self, datasize,  id, neigbors):
        global actual_mean
        global actual_counter
        global energy_con
        self.dataSize=datasize
        self.wsnSize=len(neigbors)
        self.pattern={}
        self.ch_id=id
        self.wsn=[]
        self.est_mean = 0
        self.readings=ClusterHead.readData(self,id)
        #print(id, "    ", self.readings)
        ClusterHead.generatePattern(self)
        self.neighbors=neigbors
        actual_mean += sum(self.readings)/len(self.readings)
        self.V = 3.6
        self.Itx = ((17.4 + 18.8 + 0.5 + 0.426) / 32768)
        self.batCap = 3.6
        self.ChTotalTrans=0
        actual_counter += 1

        for i in neigbors:
            s=sensor(datasize)
            s.uploadData(i)

            actual_mean+=sum(s.readings)/len(s.readings)
            #print(len(s.readings))
            actual_counter+=1
            s.setPattern(self.pattern)
            self.wsn.append(s)

    def readData(self, node_id):
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
                if count > self.dataSize:
                    break

                if " " not in readline:
                    readingList.append(float(readline))
        except IOError as e:
            print(" file cann't be found or open")
        return readingList
    def generatePattern(self):

        #self.pattern[1] = [19,24]
        #self.pattern[2] = [25, 30]
        #self.pattern[3] = [31, 36]
        #self.pattern[4] = [37, 40]
        #self.pattern[1] = [19, 26]
        #self.pattern[2] = [27, 34]
        #self.pattern[3] = [35, 40]
        self.pattern[1] = [19, 29]
        self.pattern[2] = [30, 40]


        #self.pattern[5] = [34, 37]
        #self.pattern[5] = [38, 41]
        #self.pattern[5] = [42, 45]
        #self.pattern[5] = [46, 49]

    def aggregate(self, index):
        elist=[]
        elist.append(self.readings[index])

        #print("group len", len(self.wsn))
        for i in range (0, len(self.wsn)):
            value=self.wsn[i].getNextReading(index)
            if value is not None:
                elist.append(value)

        for v1 in elist:
            for v2 in elist:
                if v1 !=v2:
                    if ClusterHead.findPattern(self, v1)==ClusterHead.findPattern(self, v2):
                        elist.remove(v2)


        self.ChTotalTrans +=len(elist)
        return elist


    def findPattern(self, value):
        for i in range(1, len(self.pattern)):
            if round_up(value)>=self.pattern[i][0] and round_up(value)<=self.pattern[i][1]:
                return i

def findAccuracy():
    sum = 0
    global test_mean
    global actual_counter
    global actual_mean
    #actual_mean = 0.0
    """for i in range(0, self.dataSize):
        for s in self.wsn:
            sum+=s.readings[i]
        actual_mean+=(sum/self.wsnSize)
        sum=0
    #actual_mean=actual_mean/self.dataSize
    #self.est_mean=self.est_mean/self.dataSize
    #print(actual_mean, "   ", self.est_mean)"""
    #actual_mean=actual_mean/actual_counter
    #print(test_mean,"    ", actual_mean)
    acc = (abs(actual_mean - test_mean) / actual_mean) * 100
    print("Accuracy:", acc)

test_mean=0
aglist=[]

def run(file_name, datasize):
    #lls=uploadData(file_name)
    s = Sink(file_name)
    global test_mean
    global actual_mean
    global aglist
    global energy_con
    #s.buildGroup()
    #s.refineGroups()

    lls=s.lls
    actual_mean=0
    test_mean=0
    counter=0
    wsnNet=[]
    sum_1=0
    temp=lls.head
    templist=[]

    while temp is not None:
        ch=ClusterHead(datasize, temp.getNodeId(), temp.getNeighbors())
        wsnNet.append(ch)
        temp=temp.next
    sum_2=0
    counter_2=0
    for i in range(0, datasize):
        for ch in wsnNet:
            sum_2+=ch.readings[i]
            counter_2+=1
            for s in ch.wsn:
                sum_2+=s.readings[i]
                counter_2 += 1
        actual_mean=actual_mean+sum_2/counter_2
        #print(sum_2/counter_2)
        sum_2=0
        counter_2=0



    for i in range(0, datasize):
        for ch in wsnNet:
            #charge = ch.Itx * (0.426 + 15) / 32768
            charge=17.4/32768
            Etx = ch.V * charge
            l=ch.aggregate(i)
            ch.batCap=ch.batCap-Etx*len(l)
            sum_1+=sum(l)/len(l)#/len(ch.aggregate(i))

            counter+=1
            for val in l:
                templist.append(val)
        #print(counter, "  ",len(templist))
        aglist.append(templist)
        #print( sum(templist)/len(templist))
        test_mean+=sum(templist)/len(templist)
        #print(sum(templist)/len(templist))
        templist = []
        counter=0
        sum_1=0
    total=0

    for ch in wsnNet:
        energy_con+=3.6-ch.batCap
        total+=ch.ChTotalTrans

        for s in ch.wsn:
            total+=s.totaltrans
            energy_con += 3.6 - s.batCap
    print("Energy Efficiency:", total/(energy_con))
    #print(test_mean, "    ", actual_mean)

def findTemporalRedundancy(th, datasize):
    counter = 0
    sum = 0
    global aglist
    sml=0
    sml=len(aglist[0])
    for val in aglist:
        if len(val)<sml:
            sml=len(val)
    for k in range(0, sml):
        for i in range(0, len(aglist) - 1):
            if abs(round(aglist[i][k]) - round(aglist[i + 1][k])) <= th:
                counter += 1
        sum += counter / datasize
        counter = 0
    print("Temporal Redundancy", sum / sml * 100)

def findSpatialRedundancy(th, dataSize):
    tspred = 0
    counter = 1
    spatial_sum = 0
    spatial_sum1 = 0
    tReadings = []
    for n in aglist:
        # print("appppppppppppppp",n)
        for k in range(0, len(n)):
            if round(n[k]) not in tReadings:
                #print(n)
                tReadings.append(round(n[k]))
                """for l in range(k + 1, len(n)):
                    if abs(round(n[k]) - round(n[l])) <= th:
                        counter += 1

                if counter > 1:
                    spatial_sum += (counter) / len(n)
                    counter = 1"""

        spatial_sum1 += 1-(len(tReadings) / len(n))
        tReadings = []
        spatial_sum = 0
        counter = 1

        # counter=counter
    # tspred += (counter / len(n))

    print("Spatial Redundancy:", spatial_sum1 / dataSize * 100)

    """tspred = 0
    counter = 0
    tRreadings = []

    for n in aglist:
        for k in range(0, len(n) - 1):
            for l in range(k + 1, len(n)):
                if abs(n[k] - n[l]) <= th:
                    counter += 1
        tspred += (counter / len(n))

        counter = 0
    print("Spatial Redundancy:", tspred / dataSize * 100)"""


def findTotalEnergyConsumption():
    global energy_con
    print("Energy Consumption", energy_con)

datasize=1100
run("wsns/500.txt", datasize)
findAccuracy()
findTemporalRedundancy(0.0,datasize)
findSpatialRedundancy(0.0, datasize)
findTotalEnergyConsumption()
"""for k in aglist:
    print(len(k), "   ",(k))"""