# Machine Learning in Action
# SVD
# CF

from numpy import *
import math
import pymysql


host = "localhost"
user = "root"
passwd = "1q2w3e"
database = "file_manage"
charset = 'utf8'
use_unicode = True

# 打开数据库连接
db_conn = pymysql.connect(host=host, user=user, passwd=passwd, db=database, charset=charset,
                          use_unicode=use_unicode)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db_conn.cursor()



def loadExData():
    # 获取所有的文件ID（即file_id）
    cursor.execute("SELECT file_id FROM file_manage_app_file;")
    file_id_tuple = cursor.fetchall()
    file_id_list = list(map(lambda x: x[0], file_id_tuple))
    returnMat = zeros((12, len(file_id_list)))  # 零矩阵,此处认为用户的编号是从1开始的

    cursor.execute("SELECT * FROM file_manage_app_user_item;")
    user_file_tuple = cursor.fetchall()
    for user_id, file_id in user_file_tuple:
        row = int(user_id)
        column = int(file_id_list.index(file_id))
        returnMat[row][column] = 1
    return file_id_list, mat(returnMat)


# 欧氏距离
# inA,inB均为列向量
def euclidSim(inA, inB):
    return 1.0 / (1.0 + linalg.norm(inA - inB))


# 基于用户相似度的推荐引擎
# 标准估分函数，返回user对item的预测评分值
# dataMat:数据矩阵
# user:用户编号
# simMeas:相似度计算方法
# item:物品编号
def standEst(dataMat, user, simMeas, item):
    n = shape(dataMat)[0]  # 读取行的维数，即用户的个数
    simTotal = 0.0
    ratSimTotal = 0.0
    for j in range(n):
        userRating = dataMat[j, item]
        if userRating == 0:
            continue
        overLap = nonzero(logical_and(dataMat[user, :].A > 0, dataMat[j, :].A > 0))[1]
        if len(overLap) == 0:
            similarity = 0
        else:
            similarity = simMeas(dataMat[user, overLap].T, dataMat[j, overLap].T)
        simTotal += similarity
        ratSimTotal += similarity * userRating
    if simTotal == 0:
        return 0
    else:
        return ratSimTotal / simTotal


# 推荐函数,top-N推荐,对用户没有评级的物品进行评分预测后，按降序排列，提取前N个物品进行推荐
# dataMat:数据矩阵
# user:用户编号，为该用户推荐
# N:top-N推荐，若没有指定值，则默认N=3
# simMeas:相似度计算方法，若没有指定值，则默认预先相似度
# estMethod:预测方法，若没有指定值，则默认标准评分预测
def recommend(dataMat, user, N=5, simMeas=euclidSim, estMethod=standEst):
    unratedItems = nonzero(dataMat[user, :].A == 0)[1]
    if len(unratedItems) == 0:
        return 'you rated everything'
    itemScores = []
    for item in unratedItems:
        estimatedScore = estMethod(dataMat, user, simMeas, item)
        itemScores.append((item, estimatedScore))
    return sorted(itemScores, key=lambda jj: jj[1], reverse=True)[:N]  # 寻找前N个未评级物品


if __name__ == '__main__':
    import time

    time_begin = time.clock()
    file_id_list, myMat = loadExData()
    
    for i in range(1, 12):

        recommend_index = recommend(myMat, i)
        index = list(map(lambda x: x[0], recommend_index))
        recommend_list = list(map(lambda x: file_id_list[x], index))
        for j in recommend_list:
            cursor.execute("INSERT INTO file_manage.file_manage_app_rec(user_id, rec_file_id) value (%s,%s)", (i, j))
            db_conn.commit()
    print("-------------------------------------------------")
    print("Use time: %s" % (time.clock() - time_begin))
