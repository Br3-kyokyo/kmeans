import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ffmpeg
from mpl_toolkits.mplot3d import Axes3D 

CLUSTERNUM = 3

def abs(v1, v2):
    return np.sqrt((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2 + (v1[1]-v2[1])**2)

def mean(result, cluster):
    x_sum, y_sum, z_sum = 0, 0, 0
    x_num, y_num, z_num = 0, 0, 0
    
    for n in np.arange(0,30):
        if(result[n, 3] == cluster):
            x_sum += result[n, 0]
            y_sum += result[n, 1]
            z_sum += result[n, 2]
            x_num += 1            
            y_num += 1
            z_num += 1
    
    
    x_mean = (x_sum/x_num)
    y_mean = (y_sum/y_num)
    z_mean = (z_sum/z_num)
    
    #rint("mean")
    #rint(x_mean)
    #rint(y_mean)
    #int(z_mean)
    
    return np.array([x_mean, y_mean, z_mean, 0])

def select_row(result, cluster):
    
    resultArray = []
    
    for n in np.arange(0, 30):
        if(result[n, 3] == cluster):
            resultArray.append(result[n])
    
    resultArray = np.array(resultArray)
    
    return resultArray


data = pd.read_csv("./kmeansdata", header=None).values

result = np.insert(data, 3, -1, axis=1)
cent_init = np.random.choice(np.arange(0,30), CLUSTERNUM)

centroid = [result[cent_init[0]], result[cent_init[1]], result[cent_init[2]]]
centroid = np.array(centroid)


while True:    
    endflag = True
    for n in np.arange(0,30):
        
        centroid_prev = result[n][3]
        
        dest0=abs(result[n], centroid[0])
        dest1=abs(result[n], centroid[1])
        dest2=abs(result[n], centroid[2])

        if(dest0 < dest1 and dest0 < dest2):
            result[n][3] = 0
        elif(dest1 < dest0 and dest1 < dest2):
            result[n][3] = 1
        else:
            result[n][3] = 2

        if(centroid_prev != result[n][3]):
            endflag = False
            
    if(endflag):
        break
        
    centroid[0] = mean(result, 0)
    centroid[1] = mean(result, 1)
    centroid[2] = mean(result, 2)
    
    print(centroid)
        

fig = plt.figure()
scatGraph = fig.add_subplot(1,1,1,projection='3d')

result_0 = select_row(result, 0)
result_1 = select_row(result, 1)
result_2 = select_row(result, 2)

x=result_0[:,0]
y=result_0[:,1]
z=result_0[:,2]
scatGraph.scatter(x, y, z, edgecolors='red', alpha=1)

x=result_1[:,0]
y=result_1[:,1]
z=result_1[:,2]
scatGraph.scatter(x, y, z, edgecolors='green', alpha=1)

x=result_2[:,0]
y=result_2[:,1]
z=result_2[:,2]
scatGraph.scatter(x, y, z, edgecolors='yellow', alpha=1)

scatGraph.set_xlabel('GDP/person')
scatGraph.set_ylabel('Population Density')
scatGraph.set_zlabel('Birthrate')

plt.show()

