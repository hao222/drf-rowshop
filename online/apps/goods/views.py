from rest_framework import mixins, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializer import GoodsSerializer
from .models import Goods
from django.shortcuts import render

# Create your views here.

#自定义pagenation分页功能
class GoodsPage(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 99


class GoodsListView(generics.ListAPIView):
    """
    商品列表页
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPage



