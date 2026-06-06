import opensim as osim
import numpy as np

def getDistanceList(data_list):
    distance_list = np.zeros(7,)

    # [右大腿骨、左大腿骨、体幹(股関節中央-胸郭)、右上腕、左上腕、右前腕、左前腕]でdistance_listを作成
    for i in range(data_list.shape[0]):
        distance_list[0] += np.sqrt(np.sum((data_list[i][4]-data_list[i][5])**2))
        distance_list[1] += np.sqrt(np.sum((data_list[i][1]-data_list[i][2])**2))
        distance_list[2] += np.sqrt(np.sum((data_list[i][0]-data_list[i][8])**2))
        distance_list[3] += np.sqrt(np.sum((data_list[i][11]-data_list[i][12])**2))
        distance_list[4] += np.sqrt(np.sum((data_list[i][14]-data_list[i][15])**2))
        distance_list[5] += np.sqrt(np.sum((data_list[i][12]-data_list[i][13])**2))
        distance_list[6] += np.sqrt(np.sum((data_list[i][15]-data_list[i][16])**2))
    distance_list = distance_list / data_list.shape[0]
    return distance_list