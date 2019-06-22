from rest_framework import mixins, generics, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .filters import GoodsFilter
from .serializer import GoodsSerializer, CategorySerializer
from .models import Goods, GoodsCategory
from django.shortcuts import render

# Create your views here.

# 自定义pagenation分页功能
class GoodsPage(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 99


class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    商品列表页   GenericViewSet  实现分页、过滤、搜索、排序
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPage
    # 俩行代替下面的get_queryset
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')   # 这些是searchfilter 搜索字段  还有 ^  以什么开头  = 完全匹配 @ 全文搜索 $正则表达式搜索
    ordering_fields = ('sold_num', 'add_time')  # 排序

    #属性  过滤 获取
    # def get_queryset(self):
    #     queryset = Goods.objects.all()  # 只有在for循环时才会真正的取出数据
    #     #request.query_params 从前端获取的  request.get
    #     price_min = self.request.query_params.get('price_min', 0)
    #     if price_min:
    #         queryset = Goods.objects.filter(shop_price__gt=int(price_min))
    #     return queryset

# RetrieveModelMixin 展示详情数据，并且返回的url 遵循 restful 不需要做任何配置。
class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    分类列表数据
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


