#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/1 9:13
# @Author  : wuhao

from rest_framework import serializers

from goods.models import Goods
from goods.serializer import GoodsSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods


##########################################
# Serializer需要自己重写create update方法#
# ModelSerializer  已经简单的实现了   ####
##########################################
class ShopCartSerializer(serializers.Serializer):
    """
    购物车商品序列化
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1, error_messages={
        "min_value":"商品数量不能小于一",
        "reruired":"必须选择一个"
    })
    # 序列化为一个商品id，并不是商品详情
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    # 此时已经处理过的数据validated_data  在serializer里面user不是直接放在request，而是在context上下文
    # 如果购物车有商品 则在数量上加1 ， 没有则创建 并返回给views
    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        # instance 是ShoppingCart 实例
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class ShopCartDetailSerializer(serializers.ModelSerializer):
    # 一个shoppingcart 对应一个商品记录
    goods = GoodsSerializer(many=False)
    class Meta:
        model = ShoppingCart
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    def generate_order_sn(self):
        # 订单号 当前时间+userid+随机数
        from random import Random
        import time
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))
        return order_sn


    def validate(self, attrs):
        # validate中添加order_sn,在view的函数perform_create  的serializer 就可以直接获取到order_sn
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderGoodsSerializer(serializers.ModelSerializer):
    """
    订单中的商品序列化类
    """
    goods = GoodsSerializer(many=False)  # 是一个外键 所以只有一个

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    """订单详情信息"""
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"

