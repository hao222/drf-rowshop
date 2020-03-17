from rest_framework import mixins, generics, viewsets, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from .filters import GoodsFilter
from .serializer import GoodsSerializer, CategorySerializer, BannerSerializer, IndexCategorySerializer, \
    HotWordsSerializer
from .models import Goods, GoodsCategory, Banner, HotSearchWords
from django.shortcuts import render

# Create your views here.

# 自定义pagenation分页功能
class GoodsPage(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

class GoodsListView(APIView):
    """
    练习
    """
    def get(self, request, format=None):
        goods = Goods.objects.all()
        goods_ser = GoodsSerializer(goods, many=True)
        return Response(goods_ser.data, status=status.HTTP_200_OK)

class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品列表页   GenericViewSet  实现分页、过滤、搜索、排序
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPage

    throttle_classes = (AnonRateThrottle, UserRateThrottle)
    # 添加token认证  只有通过认证后才可以访问此时的views
    # authentication_classes = (TokenAuthentication, )
    # 俩行代替下面的get_queryset
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')   # 这些是searchfilter 搜索字段  还有 ^  以什么开头  = 完全匹配 @ 全文搜索 $正则表达式搜索
    ordering_fields = ('sold_num', 'shop_price')  # 排序
    parser_classes = ()
    # 重写retrieve方法  修改详情 点击数 +1
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        """
        过滤 视图类里有queryset 或者有get_queryset
        对于一些复杂的过滤 排序，等 可以在这写逻辑
        :return:
        """
        pass

# RetrieveModelMixin 展示详情数据，并且返回的url 遵循 restful 不需要做任何配置。
class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    分类列表数据
    先取出一级类目 然后通过serializer序列化取出二级 三级
    外键是自身 取出sub_cat
    RetrieveModelMixin  不需要url后正则匹配 直接是restful规范
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页轮播图
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    # 获取is_tab=True（导航栏）里面的分类下的商品数据    在首页中部左展示  做下限制
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer


class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    热搜
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer