from Sink import Sink
from SinkKalmanFilter import SinkKalmanFilter
from copy import deepcopy
from SensorSimulator import SensorSimulator
import numpy as np
class myApproach:
    def __init__(self,wsnsize,theta, emax, cachelen, dataSize, net_file_name):
        self.sink=Sink(net_file_name)
        self.sink.buildGroup()
        self.sink.refineGroups()
        self.sink.refineGroups()
        self.skf=[]
        self.slist=[]
        self.dataSize=dataSize
        self.est_mean=0.0
        self.wsnSize=wsnsize
        self.totalVar=0
        self.outputlen=0
        self.TotalAgrData=0
        self.totalaggregationOutput=[]
        self.prevList=[]




        for i in range(0,wsnsize):
            skl=SinkKalmanFilter(i+1)
            sn=SensorSimulator(theta,emax,cachelen)
            sn.getSensorReadings(i+1,dataSize)
            self.slist.append((sn))
            self.skf.append((skl))




    def aggregate(self, rno, th):
        lls=self.sink.lls
        temp=lls.head
        sum=0.0
        counter=0
        agList=[]
        tlist=[]
        sum_2=0

        while (temp is not None):
            node_id=temp.getNodeId()
            sensorh=self.slist[node_id-1]
            valh=sensorh.RDR(sensorh.readings[rno])
            counter+=1
            if valh is None:
                #my code
                valh=self.skf[node_id-1].run(None)
                tlist.append(valh)

                sum+=self.skf[node_id-1].run(None)
            else:
                sum+=valh
                tlist.append(valh)
                self.skf[node_id - 1].run(sensorh.readings[rno])
            for el in temp.getNeighbors():
                sensor=self.slist[el-1]

                val=sensor.RDR(sensor.readings[rno])
                if val is None:
                    val=self.skf[el-1].run(None)
                    tlist.append(val)
                    sum += self.skf[el-1].run(None)
                else:
                    tlist.append(val)
                    sum += val
                    self.skf[el - 1].run(sensor.readings[rno])
                counter+=1
            sum_2=(max(tlist)+min(tlist))/2
            #print((max(tlist)+min(tlist))/2, "   ", tlist)
            tlist=[]
            #print("valh",valh)
            #print("val",val)
            agList.append(sum_2)
            #agList.append((sum/counter))
            #here is my code
            counter=0
            sum=0.0
            self.outputlen=len(agList)
            temp=temp.next
        sum=0
        templist_1=agList
        templist_2=[]
        """if len(self.prevList)==0:
            self.prevList=agList
            templist_2=agList
        else:
            for i in range(len(self.prevList)):
                if abs(round(self.prevList[i])-round(agList[i]))>th:
                    templist_2.append(agList[i])
                else:
                    templist_2.append(0)"""

        #print("aggregation list ", agList)
        self.TotalAgrData+=len(agList)
        #print(len(agList),"###########")

        for d in agList:
            sum+=d
        self.est_mean+=(sum/len(agList))
        #print((sum/len(agList)))
        self.totalVar+=np.var(agList)


        #print("estimated",self.est_mean)
        #print(templist_2)
        self.prevList=agList
        self.totalaggregationOutput.append(agList)

    def findTemporalRedundancy(self, th):

        counter = 0
        unsimilardata = 0
        totaldata = 0
        sum=0
        for k in range(0, len(self.totalaggregationOutput[0])):
            for i in range(0, self.dataSize-1):
                if abs(self.totalaggregationOutput[i][k] - self.totalaggregationOutput[i + 1][k]) > th:
                    counter += self.totalaggregationOutput[i][k]
                    #here is my code
                    unsimilardata+=self.totalaggregationOutput[i][k]
            #sum+=counter/self.dataSize
            sum=0
            counter=0
        print("Temporal Redundancy",sum/len(self.totalaggregationOutput[0])*100)

    def findSpatialRedundancy(self, th):
        tspred = 0
        counter = 1
        spatial_sum = 0
        spatial_sum1 = 0
        tReadings = []

        for n in self.totalaggregationOutput:
            # print("appppppppppppppp",n)
            for k in range(0, len(n) - 1):
                if round(n[k]) not in tReadings:
                    tReadings.append(round(n[k]))
                    for l in range(k + 1, len(n)):
                        if abs(round(n[k]) - round(n[l])) <= th:
                            counter += 1

                    if counter > 1:
                        spatial_sum += (round(n[k]) * counter)/ len(n)
                        #print(n[k],"  ",(n[k] * counter) )
                        counter = 1

            spatial_sum1 += 1 - len(tReadings) / len(n)
            tReadings = []
            spatial_sum = 0
            counter = 1

            # counter=counter
        # tspred += (counter / len(n))

        print("Spatial Redundancy:", spatial_sum1 / self.dataSize * 100)

        """tspred = 0
        counter = 1
        spatial_sum=0
        spatial_sum1=0
        tReadings = []

        for n in self.totalaggregationOutput:
            #print("appppppppppppppp",n)
            for k in range(0, len(n) - 1):
                if n[k]==0:
                    continue
                if n[k] not in tReadings:
                    tReadings.append(n[k])
                    for l in range(k + 1, len(n)):
                        if abs(n[k] - n[l]) < th:
                            counter +=1

                    if counter>1:
                        spatial_sum+=(n[k]*counter)#/len(n)
                        counter=1
            tReadings=[]
            spatial_sum1+=spatial_sum/sum(n)
            spatial_sum=0
            counter=1



                #counter=counter
           # tspred += (counter / len(n))


        print("Spatial Redundancy:",spatial_sum1/self.dataSize*100)
        """
        """tspred = 0
        counter = 1
        spatial_sum = 0
        spatial_sum1 = 0
        tReadings = []

        for n in self.totalaggregationOutput:
            #print("appppppppppppppp",n)
            for k in range(0, len(n) - 1):
                if n[k] == 0:
                    continue
                if round(n[k]) not in tReadings:
                    tReadings.append(round(n[k]))
                    for l in range(k + 1, len(n)):
                        if abs(round(n[k]) - round(n[l])) <= th:
                            counter += 1

                    if counter > 1:
                        spatial_sum += ( counter) / len(n)
                        # print(n[k],"  ",(n[k] * counter) )
                        counter = 1
            tReadings = []
            spatial_sum1 += spatial_sum / len(n)
            spatial_sum = 0
            counter = 1

            # counter=counter
        # tspred += (counter / len(n))

        print("Spatial Redundancy:", spatial_sum1 / self.dataSize * 100)
        """

    def findAggregationRate(self ):

        agRate=(self.TotalAgrData/(self.wsnSize*self.dataSize))*100
        #print(self.TotalAgrData, "   ", self.wsnSize,"   ", self.dataSize)
        print(" Aggregation Rate:", agRate)

    def findAccuracy(self):
        sum=00.0
        actual_mean=0.0
        for i in range(0, self.dataSize):
            for s in self.slist:
                sum+=s.readings[i]
                #print(s.readings[i])
            actual_mean+=(sum/self.wsnSize)
            #print((sum/self.wsnSize))
            sum=0
        #actual_mean=actual_mean/self.dataSize
        #self.est_mean=self.est_mean/self.dataSize
        #print(actual_mean, "   ", self.est_mean)
        acc=(abs(actual_mean-self.est_mean)/actual_mean)*100
        print("Accuracy:", acc)
        print("estemated mean",self.est_mean,"\n actual mean",actual_mean)

    def findEnergyConsumption(self):
        lls = self.sink.lls
        temp = lls.head
        sum = 0.0
        TotalTrans=0

        while (temp is not None):
            node_id = temp.getNodeId()
            sum += 3.6 - self.slist[node_id-1].batCap
            TotalTrans+=self.slist[node_id-1].totaltrans

            for el in temp.getNeighbors():
                sum += 3.6 - self.slist[el - 1].batCap
                TotalTrans += self.slist[el - 1].totaltrans
            temp=temp.next
        #print("Total:", TotalTrans)
        return sum


    def findEnergyEfficiency(self):
        sum=0
        for s in self.slist:
            sum+=s.findEnergyEfficiency()
        print("Energy Efficiency:", sum)





datasize=1100
wsnsize=500
ap=myApproach(wsnsize,0.5,0.9,10,datasize,"wsns/"+str(wsnsize)+".txt")
for i in range(0,datasize):
    ap.aggregate(i,0.01)
ap.findAccuracy()
ap.findAggregationRate()
ap.findTemporalRedundancy(0.0)
ap.findSpatialRedundancy(0.0)
ap.findEnergyEfficiency()
#ap.calculateInputReliability()
print(" Energy Consumption:",ap.findEnergyConsumption())
print((ap.totalaggregationOutput))


