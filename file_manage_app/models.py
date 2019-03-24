from django.db import models


class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=100)
    file_text = models.TextField()
    local_url = models.CharField(max_length=200)
    upload_time = models.DateTimeField()
    file_size = models.CharField(max_length=20)
    preview_file_path = models.CharField(max_length=200)
    file_type = models.CharField(max_length=20)


class Keyword(models.Model):
    key_word_id = models.AutoField(primary_key=True)
    tag_type = models.CharField(max_length=20)
    key_word = models.CharField(max_length=20)
    color = models.CharField(max_length=30)


class Searchword(models.Model):
    searchword_id = models.AutoField(primary_key=True)
    search_word = models.CharField(max_length=40)  # 记录查询的关键词
    search_count = models.PositiveIntegerField(default=0)  # 记录该条信息被查询的次数，用于展示热门搜索。用户主动输入的关键词+2，展示的相关搜索+1


class User_item(models.Model):
    user_id = models.IntegerField(primary_key=True)  # 用户的 id
    file_id = models.IntegerField(primary_key=True)  # 文件的 id


class Frequent_items(models.Model):
    main_file_id = models.IntegerField(primary_key=True)  # 主文件的 id
    relevant_file_id = models.IntegerField(primary_key=True)  # 关联文件的 id


class Rec(models.Model):
    user_id = models.IntegerField(primary_key=True)
    rec_file_id = models.IntegerField(primary_key=True)
