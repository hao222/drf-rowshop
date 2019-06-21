from rest_framework import generics
import django_filters
from goods.models import Goods

# 自定义商品过滤器   lookup_expr  expr 执行
class GoodsFilter(django_filters.rest_framework.FilterSet):
    min_price = django_filters.rest_framework.NumberFilter(field_name="shop_price", lookup_expr='gte')
    max_price = django_filters.rest_framework.NumberFilter(field_name="shop_price", lookup_expr='lte')

    class Meta:
        model = Goods
        fields = ['min_price', 'max_price']
