import pymysql

def loadDataSet():
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

	cursor.execute("SELECT user_id FROM file_manage_app_user_item GROUP BY user_id;")
	user_id_list = cursor.fetchall()
	data = []
	for user_id in user_id_list:
	    # print(news_id[0])
	    cursor.execute("SELECT file_id FROM file_manage_app_user_item WHERE user_id=%s;", user_id[0])
	    file_id_list = cursor.fetchall()
	    file = []
	    for each_file in file_id_list:
	        file.append(each_file[0])
	    data.append(file)

	cursor.execute("SELECT file_id FROM file_manage_app_user_item GROUP BY file_id;")
	file_id_list = cursor.fetchall()
	candidates = []
	for each_file in file_id_list:
	    candidates.append(each_file[0])

	db_conn.close()  # 关闭数据库连接
	return data, candidates

