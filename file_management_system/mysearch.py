from haystack.generic_views import SearchView
from file_manage_app.models import File, Keyword, Searchword
from django.http import Http404
from django.core.paginator import InvalidPage, Paginator
from haystack.query import SearchQuerySet
import difflib
import numpy as np
from django.db.models import F


class MySearchView(SearchView):
    def get_queryset(self):
        queryset = super(MySearchView, self).get_queryset()
        # further filter queryset based on some set of criteria
        # return queryset.filter(pub_date__gte=date(2015, 1, 1))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        # 相关推荐，推荐同类型的文件
        # 找出查询

        # 相关搜索
        releva_arr = np.array(Searchword.objects.all().values_list())
        # 根据搜索次数取top-10作为热点搜索
        top_hot_n = 10
        if releva_arr.shape[0] < top_hot_n:
            top_hot_n = releva_arr.shape[0]
        if top_hot_n == 0:
            context['hot_spot'] = ''
        else:
            temp = list(releva_arr[np.argpartition(releva_arr[:,-1].astype(int), -top_hot_n)[-top_hot_n:], 1])
            temp.reverse()
            context['hot_spot'] = enumerate(temp)  # 按照搜索次数从高到低取前10


        sim_arr = np.array(
            list(map(lambda x: difflib.SequenceMatcher(None, context['query'], x).quick_ratio(), releva_arr[:, 1])))
        K = 3
        index = np.argpartition(sim_arr, -K)[-K:]  # 展示相关联的前K个搜索关键词，目前暂时不设置相似度阈值 TODO：
        # 相关联的搜索词的次数 +1
        for i in releva_arr[index, 0]:
            Searchword.objects.filter(searchword_id=int(i)).update(search_count=F('search_count') + 1)

        temp = list(releva_arr[index, 1])  # 相关联的关键词
        temp.reverse()
        context['releva_search'] = temp  # 相关联的关键词

        if len(Searchword.objects.filter(search_word=context['query'])) == 0:  # 若查询结果为空，则说明输入的是新的关键词
            Searchword.objects.create(search_word=context['query'], search_count=1)  # 添加记录，并设置查询次数为 1
        else:  # 用户输入的关键词已在搜索历史列表中，说明该关键词可以很好地描述用户需求信息的特征，则使其次数+2，
            Searchword.objects.filter(search_word=context['query']).update(search_count=F('search_count') + 2)  # 更新次数

        return context
