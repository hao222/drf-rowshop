#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import Q

from goods.models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand, IndexAd, HotSearchWords

__author__ = "hao"

from rest_framework import serializers


class CategorySerializer3(serializers.ModelSerializer):
    """
    商品类别序列化  三级分类
    """
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    """
    商品类别序列化  二级分类
    """
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """一级分类"""
    sub_cat = CategorySerializer2(many=True)  #many = True  多个 不能漏掉
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image", )


#让外键的数据也显示出来
class GoodsSerializer(serializers.ModelSerializer):
    # related_name 名称
    # 直接取出外键所包含的字段内容
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    """
    轮播图
    """
    class Meta:
        model = Banner
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"

class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    # 由于获取商品的时候 是通过第三类别最小分类下的商品  所以需要自己定义个函数方法
    goods = serializers.SerializerMethodField()
    # 取出二级商品分类
    sub_cat = CategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id=obj.id)|Q(category__parent_category__parent_category_id=obj.id))
        # 对商品进行序列化
        # 当serializer里嵌套serializer 的时候 会出现域名不会自动加上的问题，主要在于跨serializer，上下文指示不明，需要重新声明一下。
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context["request"]})

        return goods_serializer.data

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            good_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context["request"]}).data
        return goods_json

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = "__all__"
