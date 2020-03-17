from django.db.models import Q
from rest_framework import generics
import django_filters
from goods.models import Goods

# 自定义商品过滤器   lookup_expr  expr 执行
class GoodsFilter(django_filters.rest_framework.FilterSet):
    pricemin = django_filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name="shop_price", lookup_expr='lte')
    # name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')
    top_category = django_filters.NumberFilter(field_name="category", method='top_category_filter')

    # 查找到第一类别下的所有商品
    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)
                               |Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        # 是否是热销产品   只需要加入is_hot
        fields = ['pricemin', 'pricemax', 'is_hot']
