from Sink import Sink
from SinkKalmanFilter import SinkKalmanFilter
import random
from copy import deepcopy
from SensorSimulator import SensorSimulator
import numpy as np
class myApproach:
    def __init__(self,wsnsize,theta, emax, cachelen, dataSize, net_file_name):
        self.sink=Sink(net_file_name)
        self.sink.buildGroup()
        self.sink.refineGroups()
        self.sink.refineGroups()
        self.sink.lls.printLinkedList()
        self.skf=[]
        self.slist=[]
        self.dataSize=dataSize
        self.est_mean=0.0
        self.wsnSize=wsnsize
        self.totalVar=0
        self.outputlen=0
        self.TotalAgrData=0
        self.totalaggregationOutput=[]



        for i in range(0,wsnsize):
            skl=SinkKalmanFilter(i+1)
            sn=SensorSimulator(theta,emax,cachelen)
            sn.getSensorReadings(i+1,dataSize)
            self.slist.append((sn))
            self.skf.append((skl))




    def aggregate(self, rno):


        lls=self.sink.lls
        temp=lls.head
        sum_1=0.0
        counter=0
        agList=[]
        max_minList=[]
        pvalh=0
        pvalc=0
        total_max_minList=[]

        while (temp is not None):
            node_id=temp.getNodeId()
            sensorh=self.slist[node_id-1]
            valh=sensorh.RDR(sensorh.readings[rno])
            counter+=1
            if valh is None:
                #my code
                valh=self.skf[node_id-1].run(sensorh.readings[rno])
                max_minList.append(valh)
                #sum+=self.skf[node_id-1].run(None)
            else:
                sum_1+=valh
                max_minList.append(valh)
                self.skf[node_id - 1].run(sensorh.readings[rno])
            for el in temp.getNeighbors():
                sensor=self.slist[el-1]

                val=sensor.RDR(sensor.readings[rno])
                if val is None:
                    val=self.skf[el-1].run(sensor.readings[rno])
                    sum_1 += val
                    max_minList.append(val)
                else:
                    sum_1 += val
                    max_minList.append(val)
                    self.skf[el - 1].run(sensor.readings[rno])
                counter+=1

            agList.append((sum_1/counter))
            sum_max_min=(max(max_minList)+min(max_minList))/2
            total_max_minList.append(sum_max_min)
            #print("max_min",sum_max_min)
            #print(max_minList)
            max_minList=[]
            #here is my code
            #if valh :
                #agList.append(valh)
            #else:
                #agList.append((sum / counter))
            counter=0
            sum_1=0.0
            self.outputlen=len(agList)
            temp=temp.next
        sum_1=0
        self.TotalAgrData+=len(agList)
        #print(len(agList),"###########")
        for d in agList:
            sum_1+=d
        #self.est_mean+=(sum/len(outlist))
        #print((sum/len(agList)))
        #self.totalVar+=np.var(agList)
        outlist=[]
        #print(agList)
        for i in range(0, len(total_max_minList)-1):
            for k in range(i+1, len(total_max_minList)):
                if round(total_max_minList[i])-round(total_max_minList[k])==0:
                    if total_max_minList[i]>total_max_minList[k]:
                        total_max_minList[k]=0
                    elif total_max_minList[i]<total_max_minList[k]:
                        total_max_minList[i] = 0
                    else:
                        total_max_minList[k] = 0

        sum_2=0
        count=0
        for i in total_max_minList:
           outlist.append(round(i))
           if i > 0:
               sum_2 += i
               count += 1


        self.est_mean += sum_2/count #(sum(outlist) / len(outlist))
        sum_2=0
        count=0




        #print("estimated",self.est_mean)
        #here i add
        #while i < len(outlist):
        """for r in outlist:
            if r not in self.totalaggregationOutput:
                self.totalaggregationOutput.append(outlist)"""

        #print("aglist",agList)
        self.totalaggregationOutput.append(outlist)
        #print(outlist)
        total_max_minList=[]
        #print("total aggregation list",self.totalaggregationOutput)

    def findTemporalRedundancy(self, th):

        counter = 0
        unsimilardata = 0
        totaldata = 0
        sum=0
        sml = 0
        finlaList=[]
        """sml = len(self.totalaggregationOutput[0])
        for val in self.totalaggregationOutput:
            if len(val) < sml:
                sml = len(val)
        for l in self.totalaggregationOutput:
            for i in range(0, len(l)-sml):
                l.append(0)
            finlaList.append(l)"""

        for k in range(0, len(self.totalaggregationOutput[0])):

            for i in range(0, self.dataSize-1):
                if self.totalaggregationOutput[i][k]==0:
                    continue
                if abs(round(self.totalaggregationOutput[i][k]) - round(self.totalaggregationOutput[i + 1][k]))<=th:
                    counter += 1

            sum+=counter/self.dataSize

            counter=0

        print("Temporal Redundancy",sum/len(self.totalaggregationOutput[0])*100)

    def findSpatialRedundancy(self, th):

        tspred = 0
        counter = 1
        spatial_sum = 0
        spatial_sum1 = 0
        tReadings = []

        for n in self.totalaggregationOutput:
            #print("appppppppppppppp",n)
            for k in range(0, len(n)):
                if round(n[k]) not in tReadings:
                    tReadings.append(round(n[k]))
                elif n[k]==0:
                    tReadings.append(n[k])
                    """for l in range(k + 1, len(n)):
                        if abs(round(n[k]) - round(n[l])) <= th:
                            counter += 1
                        if counter > 1:
                            spatial_sum += (round(n[k]) * counter)/ len(n)
                            #print(n[k],"  ",(n[k] * counter) )
                            counter = 1"""

            #print(len(tReadings),"    ",len(n))
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
                if n[k] not in tReadings:
                    tReadings.append(n[k])
                    for l in range(k + 1, len(n)):
                        if abs(n[k] - n[l]) < th:
                            counter +=1

                    if counter>1:
                        spatial_sum+=(n[k]*counter)/len(n)
                        counter=1
            tReadings=[]
            spatial_sum1+=spatial_sum/sum(n)
            spatial_sum=0
            counter=1



                #counter=counter
           # tspred += (counter / len(n))


        print("Spatial Redundancy:",spatial_sum1/self.dataSize*100)
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
        #print("estemated mean",self.est_mean,"\n actual mean",actual_mean)

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
wsnsize=125
ap=myApproach(wsnsize,0.1,0.2,5,datasize,"wsns/"+str(wsnsize)+".txt")
for i in range(0,datasize):
    ap.aggregate(i)
#print(ap.totalaggregationOutput)
ap.findAccuracy()
ap.findAggregationRate()
ap.findTemporalRedundancy(0.0)
ap.findSpatialRedundancy(0.0)
ap.findEnergyEfficiency()
#ap.calculateInputReliability()
print(" Energy Consumption:",ap.findEnergyConsumption())


