#!/usr/bin/env python
# -*- coding: utf-8 -*-
from goods.models import Goods, GoodsCategory, GoodsImage

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
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = "__all__"

