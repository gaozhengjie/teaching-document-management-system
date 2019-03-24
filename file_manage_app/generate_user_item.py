# 时间：2018年4月28日18:44:55
# 作用：用于伪造数据，生成用户-文件阅读表


import pymysql
import numpy as np
import random


host = "localhost"
user = "root"
passwd = "1q2w3e"
database = "file_manage"
charset = 'utf8'
use_unicode = True

# 打开数据库连接
db_conn = pymysql.connect(host=host, user=user, passwd=passwd, db=database, charset=charset, use_unicode=use_unicode)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db_conn.cursor()

# 获取所有的文件ID（即file_id）
cursor.execute("SELECT file_id FROM file_manage_app_file;")
file_id_list = cursor.fetchall()
user_count = 11
user_id_list = list(range(1, user_count+1))
cursor.execute("DELETE FROM file_manage_app_user_item;")  # 清空用户物品表
db_conn.commit()
for file_id in file_id_list:
	# 随机选取n个用户阅读该文章
	user_id_count = np.random.randint(0,user_count)  # 总共11个用户，随机选取n个
	user_id_sample = random.sample(user_id_list, user_id_count)  # 不重复取样
	for user_id in user_id_sample:
		try:
			cursor.execute("INSERT INTO file_manage_app_user_item(user_id, file_id) value (%s,%s)", (user_id, file_id))
		except Exception as err:
			print(str(err))
db_conn.commit()