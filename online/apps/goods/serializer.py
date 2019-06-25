#!/usr/bin/env python
# -*- coding: utf-8 -*-
from goods.models import Goods, GoodsCategory

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


#让外键的数据也显示出来
class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Goods
        fields = "__all__"

