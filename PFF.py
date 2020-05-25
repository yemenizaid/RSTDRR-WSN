from SetSimilaritySearch import all_pairs
import math
import numpy as np
class sensor:

    def __init__(self, setsSize, SNo,redundantthreshold, dataSize, similarityThreshold, fname):
        self.data=[]
        self.sensorNo=SNo
        self.fname=fname
        self.variance = 0
        self.batCap = 3.6
        self.variance = 0
        self.V = 3.6
        self.Itx = ((17.4 + 18.8 + 0.5 + 0.426) / 32768)
        self.DetaT = 5
        self.setsSize=setsSize
        self. aggregatedReadings={}
        self.similarityThreshold = similarityThreshold
        self.redundantthreshold = redundantthreshold
        self.dataSize=dataSize
        self.data=sensor.uploadData(self, SNo)
        sensor.localAggregation(self)
        #print("Energy:", len(self.aggregatedReadings))

    def findVariance(self):
        self.variance=np.var(self.data)
        return self.variance

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
                    readingList.append(float(readline))
        except IOError as e:
            print(" file cann't be found or open")
        # readingList=refineData(readingList)

        return readingList

    def getData(self):
        sensor.uploadData(self)
        return self.data

    def findEnergyConsumption(self):

        #charge= self.Itx*(0.426+15)/32768
        charge = 17.4 / 32768
        Etx = self.V * charge
        self.batCap = self.batCap - Etx

    def localAggregation(self ):

        redundant=False
        if len(self.data)==0:
            return
        for i in range(0, int(self.dataSize/self.setsSize)):
            temp = []

            for j in range (i*self.setsSize, (i+1)*self.setsSize):
                if len(temp)==0:
                    temp.append((self.data[j],1))
                    sensor.findEnergyConsumption(self)
                else:
                    for k in range(0, len(temp)):
                        value=temp[k][0]
                        if abs(self.data[j]-value)<= self.redundantthreshold:
                            temp[k]=(temp[k][0],temp[k][1]+1)
                            redundant = True
                            break
                    if not redundant:
                        sensor.findEnergyConsumption(self)
                        temp.append((self.data[j],1))
                redundant = False
            self.aggregatedReadings[i]=temp



class CHaggregator:

    def __init__(self, wsnSize,  setsSize, redundantthreshold, dataSize, similarityThreshold, fname):
        self.wsn=[]
        self.wsnSize=wsnSize
        self.b_totalavge=0
        self.a_totalavge=0
        self.totalvar=0
        self.outputlen=0
        self.totalaggregationOutput=[]
        self.totalEnergyCon=0

        acc=[]

        for i in range(0, self.wsnSize):
            s=sensor(setsSize, i+1,redundantthreshold, dataSize, similarityThreshold, fname)

            if len(s.data)>0:
                self.totalEnergyCon+=3.6-s.batCap
                self.wsn.append(s)
        sum=0
        for i in range(0, dataSize):
            for s in self.wsn:
                sum += s.data[i]
                #print(s.readings[i])
            self.b_totalavge += (sum / self.wsnSize)
            sum = 0

    def findAvg(self, data):
        return sum(data)/len(data)

    def findSimilarity(self,datasize, setsize, dictsets):
        sets=[]
        tcount=0
        #form sets from dictionary

        for i in range(0, int(datasize / setsize)):
            for j in range(0, len(self.wsn)):
                s = self.wsn[j].aggregatedReadings[i]
                sets.append(CHaggregator.formSet(self, s))

            pairs = all_pairs(sets, similarity_func_name="jaccard", similarity_threshold=self.wsn[0].similarityThreshold)
            simililartyPairs=list(pairs)
            #print(sets)

            pruneList = []
            for k in range(0, len(simililartyPairs)):

                if sets[simililartyPairs[k][1]] not in pruneList:
                    pruneList.append(sets[simililartyPairs[k][1]])

            for l in pruneList:
                sets.remove(l)
            temp=[]
            for i in range(0, len(pruneList)):
                temp.append(pruneList[i][0])
            self.outputlen=len(temp)

            self.totalvar+=np.var(temp)
            temp=[]

            #print(sets)
            #print(sets)
            for e in sets:
                for el in e:
                    temp.append(el)
            self.a_totalavge += sum(temp)/len(temp)
            #print(temp)
            self.totalaggregationOutput.append(temp)
            tcount+=len(temp)
            temp=[]
            sets=[]
            count=0
        #self.a_totalavge/=int(datasize / setsize)

        print("Accuracy:", (abs(self.b_totalavge - self.a_totalavge)/self.b_totalavge)*100)
        print("Energy Efficiency:",tcount/datasize/self.totalEnergyCon)


    def formSet(self, tuple_list):
        temp=[]
        for i in range(len(tuple_list)):
            temp.append(tuple_list[i][0])
        #print("Temp:", temp)
        return temp

    def findTemporalRedundancy(self,th, datasize):
        counter = 0
        sum = 0
        sml = 0
        sml = len(self.totalaggregationOutput[0])
        for val in self.totalaggregationOutput:
            if len(val) > sml:
                sml = len(val)
        #print("smallest:", sml)
        for i in range(0, len(self.totalaggregationOutput)):
            for k in range(0, sml-len(self.totalaggregationOutput[i])):
                self.totalaggregationOutput[i].append(0)
            #print(self.totalaggregationOutput[i])
        for k in range(0, sml):
            for i in range(0, len(self.totalaggregationOutput) - 1):
                if abs(round(self.totalaggregationOutput[i][k] )- round(self.totalaggregationOutput[i + 1][k])) <= th:
                    counter += 1
            sum += counter / datasize
            #print(counter)
            counter = 0
        print("Temporal Redundancy", sum /sml  * 100)

    def findSpatialRedundancy(self, th, dataSize):
        '''tspred = 0
        counter = 0
        sum = 0
        unwanted=0
        tRreadings = []

        for n in self.totalaggregationOutput:
            for k in range(0, len(n) - 1):
                for l in range(k + 1, len(n)):
                    if abs(n[k] - n[l]) <= th:
                        counter += 1
                        unwanted+=n[k]
                        # here to check
                    else:
                        sum+=n[k]
            #tspred += (counter / len(n))
            tspred += (unwanted/sum)
            print("unwanted ",unwanted,"        ","sum", sum)

            counter = 0
            sum=0
            unwanted=0
        print("Spatial Redundancy:", tspred / dataSize * 100)
        '''
        tspred = 0
        counter = 1
        spatial_sum = 0
        spatial_sum1 = 0
        tReadings = []

        for n in self.totalaggregationOutput:
            #print("appppppppppppppp", n)
            for k in range(0, len(n)):
                if round(n[k]) not in tReadings:
                    tReadings.append(round(n[k]))
                    """for l in range(k + 1, len(n)):
                        if abs(round(n[k]) - round(n[l])) <= th:
                            counter += 1

                    if counter > 1:
                        spatial_sum += (n[k] * counter) / len(n)
                        counter = 1"""
            #print(n)
            spatial_sum1 += 1 - (len(tReadings) / len(n))
            tReadings = []
            spatial_sum = 0
            counter = 1

            # counter=counter
        # tspred += (counter / len(n))

        print("Spatial Redundancy:", spatial_sum1 / dataSize * 100)
    def refineData(self, data):
        temp=[]
        llen=len(temp)
        for e in data:
            if e not in temp:
                temp.append(e)
        return temp

    def round_up(self, n, decimals=0):
        multiplier = 10 ** decimals
        return math.ceil(n * multiplier) / multiplier

datasize=1100

s=CHaggregator(50,5,0.03,datasize,0.35, None)

#s.findRedundancyPercentage()
s.findSimilarity(datasize,5,None)
s.findSpatialRedundancy(0.0, datasize)
s.findTemporalRedundancy(0.0, datasize)

print("Energy Consumption", s.totalEnergyCon)

