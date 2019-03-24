# 时间：2018年4月28日18:54:12
# 功能：以每一个用户看过的所有文章为整体，使用apriori

import loaddata
import time
import collections
import pymysql


def findFrequency(data_set, candidates, min_sup=0.7):
    fre_list = {}
    for i in candidates:
        temp = []
        count = 0
        for j in data_set:
            if i in j:
                count += 1
                temp.extend(j)
        # 统计每个名称出现的频次
        count_list = list(collections.Counter(temp).items())
        temp_fre_list = []
        for k in count_list:
            if k[1] / count >= min_sup:
                temp_fre_list.extend([k[0]])
        temp_fre_list.remove(i)
        if len(temp_fre_list) > 0:
            fre_list[i] = temp_fre_list
    return fre_list


if __name__ == '__main__':
    time_begin = time.clock()

    host = "localhost"
    user = "root"
    passwd = "1q2w3e"
    database = "file_manage"
    charset = 'utf8'
    use_unicode = True
    db_conn = pymysql.connect(host=host, user=user, passwd=passwd, db=database, charset=charset,
                              use_unicode=use_unicode)  # 打开数据库连接
    cursor = db_conn.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor

    data_set, candidates = loaddata.loadDataSet()
    F = findFrequency(data_set, candidates, 0.5)

    # with open('FrequentItems.txt', 'w', encoding='utf-8') as fp:
    #     fp.write(str(F))
    cursor.execute("DELETE FROM file_manage.file_manage_app_frequent_items")  # 每次挖掘频繁项之前先将表清空

    for i in F.items():
        for j in i[1]:
            cursor.execute("INSERT INTO file_manage.file_manage_app_frequent_items(main_file_id, relevant_file_id) value (%s,%s)",
                           (i[0], j))
            db_conn.commit()

    db_conn.close()
    print("Use time: %s" % (time.clock() - time_begin))
