#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/28 11:21
# @Author  : wuhao

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from goods.serializer import GoodsSerializer
from .models import UserFav, UserLeavingMessage, UserAddress


class UserFavDetailSerializer(serializers.ModelSerializer):
    """
    用户收藏详情页
    """
    # 通过商品id 获取收藏的商品， 需要嵌套商品的序列化
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):
    """
    用户收藏
    """
    # 用户收藏时不应该出现user字段， user应该是自动获取登录的user
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        # 验证联合唯一性   这个写在meta 里面 意为 多个字段。
        validators = [
            UniqueTogetherValidator(
                queryset = UserFav.objects.all(),
                fields = ("user", "goods"),
                message = "已经收藏"
            )
        ]
        model = UserFav
        # 如果需要添加一个商品删除功能，需要返回一个id
        fields = ("user", "goods", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    """
    用户留言
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UserLeavingMessage
        fields = ("id", "user", "message_type", "subject", "message", "file", "add_time")


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "address", "signer_name", "add_time", "signer_mobile", "district")

