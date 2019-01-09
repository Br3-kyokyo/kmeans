# パターン認識プログラミング課題 K-means法
# s1611133 佐々木恭平 
#  
# 時々、クラスタの数が0になってZeroDivisionErrorがおきます、すみません
# CLUSTERNUMの値を変更すればクラスタ数を変更できるようになっています 
#

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 

#クラスタ数指定
CLUSTERNUM = 4

#関数宣言
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
    
    return np.array([x_mean, y_mean, z_mean, 0])

def select_row(result, cluster):
    
    resultArray = []
    
    for n in np.arange(0, 30):
        if(result[n, 3] == cluster):
            resultArray.append(result[n])
    
    resultArray = np.array(resultArray)
    
    return resultArray


##以下メイン部##

#データ読み込み
data = pd.read_csv("./kmeansdata", header=None).values
#各データにクラスタ番号を紐付け
result = np.insert(data, 3, -1, axis=1)
#セントロイドの初期値をランダムに決定(データの座標を拝借)
cent_init = np.random.choice(np.arange(0,30), CLUSTERNUM)
centroid = []
for cluster in np.arange(0, CLUSTERNUM):
    centroid.append(result[cent_init[cluster]])
centroid = np.array(centroid)

#メインループ
while True:    
    endflag = True #クラスタ番号の変更を検知したらendflagがFalseになる
    
    #全データについてクラスタ番号を決定
    for n in np.arange(0,30):
        
        centroid_prev = result[n][3]

        #各セントロイドとの距離を算出
        dest = []
        for cluster in np.arange(0, CLUSTERNUM):
            dest.append(abs(result[n], centroid[cluster]))
        dest = np.array(dest)
       
        #最も近いセントロイドを選出しセントロイド番号を更新
        for cluster in np.arange(0, CLUSTERNUM):
            if(min(dest) == dest[cluster]):
                result[n][3] = cluster           
            
        if(centroid_prev != result[n][3]):
            endflag = False
            
    if(endflag):
        break 
    
    #セントロイド更新
    for cluster in np.arange(0, CLUSTERNUM):
        centroid[cluster] = mean(result, cluster)
    


##以下描画フェーズ##
fig = plt.figure()
scatGraph = fig.add_subplot(1,1,1,projection='3d')

clustercol = ['red', 'green', 'yellow', 'blue', 'black', 'magenta']

for cluster in np.arange(0, CLUSTERNUM):
    x = []
    result_axis = np.array(select_row(result, cluster))
    for axis in np.arange(0, 3):
        x.append(result_axis[:,axis])
    x = np.array(x)
    scatGraph.scatter(x[0], x[1], x[2], edgecolors=clustercol[cluster], alpha=1)

scatGraph.set_xlabel('GDP/person')
scatGraph.set_ylabel('Population Density')
scatGraph.set_zlabel('Birthrate')

plt.show()