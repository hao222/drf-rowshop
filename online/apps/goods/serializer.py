#!/usr/bin/env python
# -*- coding: utf-8 -*-
from goods.models import Goods, GoodsCategory

__author__ = "hao"

from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


#让外键的数据也显示出来
class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Goods
        fields = "__all__"
