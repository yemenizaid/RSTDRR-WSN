import math
def getData(sensor_id, dataSize):
    readingList = []
    count = 0

    try:
        f = open("datasets_5/Sensor_" + str(sensor_id) + ".txt", 'r')
        while True:
            readline = f.readline()
            if readline == '':
                break
            count += 1
            if count > dataSize:
                break

            if " " not in readline:
                readingList.append(float(readline))
                #print(sensor_id)
    except IOError as e:
        print(" file cann't be found or open")
    # readingList=refineData(readingList)
    return readingList

def getTemporalRedundancy(tlist, th):

    counter=0
    for i in range (0, len(tlist)-1):
        if abs(round(tlist[i+1])-round(tlist[i]))<=th:
            counter+=1
    #print((counter/len(tlist)))
    return (counter/len(tlist))


def getSpatialRedundancy(wsn, datasize, th):
    """tspred=0
    counter=0
    tRreadings=[]
    for n in range(0, datasize):
        for m in range(0, len(wsn)-1):
            tRreadings.append(wsn[m][n])

        for k in range(0, len(tRreadings)-1):
            for l in range(k+1, len(tRreadings)):
                if abs(tRreadings[k]-tRreadings[l])<=th:
                    counter+=1

            #counter=counter/k
        tspred+=(counter/len(tRreadings))
        counter=0
        tRreadings=[]
    return tspred"""
    tspred = 0
    counter = 1
    counter_1=0
    spatial_sum = 0
    spatial_sum1 = 0
    tReadings = []
    treading_1=[]
    for n in wsn:
        #print("",n)
        for k in range(0, len(n)):
            #tReadings.append(round(n[k]))
            #print(round(n[k]), "      ", n[k])
            if round(n[k]) not in tReadings:
                tReadings.append(round(n[k]))
                """for l in range(k + 1, len(n)):

                    if abs(round(n[k]) - round(n[l])) <= th:
                        counter += 1

                if counter > 1:
                    spatial_sum += (counter) / len(n)
                    counter_1+=1
                    #print(( counter) / len(n) )
                    counter = 1
        #print(1-(len(tReadings)/len(n)))
        """

        spatial_sum1 += (1-(len(tReadings)/len(n)))#spatial_sum#*100 # / len(n)
        tReadings = []
        treading_1 = []
        #print("sum:", spatial_sum)
        spatial_sum = 0
        counter = 1

        # counter=counter
    # tspred += (counter / len(n))/
    print("Spatial Redundancy:", (spatial_sum1/datasize*100))#datasize )

datasize=700
wsnsize=500
wsnreadings=[]
sum_1=0
splist=[]
th=0.0
for i in range (0, wsnsize):
    wsnreadings.append(getData(i+1, datasize))
for i in range(0, len(wsnreadings[0])):
    templist=[]
    for n in wsnreadings:
        templist.append(n[i])
    #print(templist)

    splist.append(templist)


for j in range (0, wsnsize):
    sum_1+=getTemporalRedundancy(wsnreadings[j], th)
print("Temporal Redundancy:", sum_1/wsnsize*100)
getSpatialRedundancy(splist, datasize, th)
#print ("Spatial Redundancy:", getSpatialRedundancy(splist, datasize, th)/datasize *100)
