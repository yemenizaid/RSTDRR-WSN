from UploadData import readfile, getData

from KalmanFilter import KalmanFilter
import math
from common import Q_discrete_white_noise
import numpy as np
#import matplotlib.pyplot as pl
def round_up( n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

class SensorSimulator:
    def __init__(self, theta, emax, cachelen):
        self.cache=[]
        self.readings=[]
        self.totaltrans=0
        self.cacheLen=cachelen
        self.theta=theta
        self.emax=emax
        self.counter=0
        self.correcteddata=[]
        self.totalTransferredData=0
        r_std, q_std = 1., 0.003
        self.kf = KalmanFilter(dim_x=2, dim_z=1)
        self.kf.x = np.array([[19], [0]])  # position, velocity
        self.kf.F = np.array([[1, 1], [0, 1]])
        self.kf.R = np.array([[r_std ** 2]])  # input noise
        self.kf.H = np.array([[1., 0.]])
        self.kf.P = np.diag([0.001 ** 2, 0])
        self.kf.Q = Q_discrete_white_noise(2, 1, q_std ** 2)
        self.est_list=[]
        self.counter=0
        self.batCap=3.6
        self.variance=0
        self.V=3.6
        self.Itx=((17.4+18.8+0.5+0.426)/32768)
        self.DetaT=5

    def getSensorReadings(self,sensor_id, dataSize):
        self.readings=getData(sensor_id, dataSize)
        return self.readings



    def RDR(self, sensorReading):
        distance=sum=0.0
        transmitted_counter=0
        corr=0.0
        list_1=[]
        est_list=[]

        s=0
        if len(self.cache)<=self.cacheLen:
            self.cache.append(sensorReading)
            SensorSimulator.findEnergyConsumption(self)
            self.correcteddata.append(sensorReading)

            self.totaltrans+=1
            #print(sensorReading)
            self.kf.predict()
            self.kf.update([sensorReading])
            return sensorReading
        else:
            if sensorReading==self.cache[self.cacheLen-1]:
                self.correcteddata.append(sensorReading)
                return
            else:
                for i in range (0, self.cacheLen):
                    distance+=pow(sensorReading-self.cache[i],2)
                    sum+=self.cache[i]
                distance=math.sqrt(distance)
                corr=1-distance/sum
                est=self.kf.predict()
                self.est_list.append(est[0])

                estval=est[0][0]
                self.kf.update(est[0][0])
                #print(sensorReading - estval, ", ", corr)
                if corr<self.theta:
                    sensorReading=est[0][0]
                    self.cache.pop(0)
                    self.cache.append(sensorReading)
                    self.counter+=1
                    SensorSimulator.findEnergyConsumption(self)
                    self.correcteddata.append(sensorReading) ####################

                    self.totaltrans += 1
                    #print(sensorReading)
                    return sensorReading
                else:
                    #print(sensorReading - estval)
                    if abs(sensorReading - estval) < self.emax:
                        self.correcteddata.append(sensorReading)
                        exit
                    else:
                        self.cache.pop(0)
                        self.cache.append(sensorReading)
                        self.counter+=1
                        SensorSimulator.findEnergyConsumption(self)
                        self.correcteddata.append(sensorReading)

                        self.totaltrans += 1
                        #print(sensorReading)
                        return sensorReading

    def findVariance(self):
        self.variance=np.var(self.readings)
        return self.variance


    def findEnergyEfficiency(self):
       # print(self.totalTransferredData)
        #print(3.6-self.batCap, 0)
       # print("Energy Efficiency:", self.totalTransferredData/(3.6-self.batCap))
        return 1#self.totalTransferredData/(3.6-self.batCap)


    def findEnergyConsumption(self):

        #charge= self.Itx*(0.426+15)/32768
        charge=17.4/32768
        Etx = self.V * charge
        self.batCap=self.batCap-Etx
        #print(Etx*100, "  ", self.batCap)
        #print("for one message",Etx)



def getData(sensor_id, dataSize):
    readingList = []
    count = 0

    try:
        f = open("datasets/Sensor_" + str(sensor_id) + ".txt", 'r')
        while True:
            readline = f.readline()
            if readline == '':
                break
            count += 1
            if count > dataSize:
                break

            if " " not in readline:
                readingList.append(float(readline))
    except IOError as e:
        print(" file cann't be found or open")
    # readingList=refineData(readingList)
    return readingList
#ss=SensorSimulator(0.5,0.3,5)
#list=ss.getSensorReadings(7,700)
#print()#readfile(f_name="datasets/sensor_1.txt")#ss.readings

ss=SensorSimulator(0.5,0.001,5)
ss.findEnergyConsumption()
ss=SensorSimulator(0.5,0.001,5)
ss.readings=getData(1,400)
list=ss.getSensorReadings(1,700) #readfile(f_name="datasets/sensor_1.txt")#ss.readings
list_1=[]
print(list)
for value in list:
    val=ss.RDR(value)
    if val is not None:
        list_1.append(val)

print("corrected",ss.totaltrans)

print("Data with Error:", ss.readings)
ss.findEnergyEfficiency()
""""
ss.findVariance()
print("length",len(list_1))
pl.xlabel("Samples")
pl.ylabel("Temperature")
pl.plot(list,label="Real data")
pl.plot(list_1, label="Filtered Data")
pl.plot(ss.est_list, label="Estimated Value")
pl.legend()
pl.show()"""








