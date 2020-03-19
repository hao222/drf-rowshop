#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/1 9:13
# @Author  : wuhao

from rest_framework import serializers

from goods.models import Goods
from goods.serializer import GoodsSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient

from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.GoodsDetail import GoodsDetail

from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.response.AlipayTradePagePayResponse import AlipayTradePagePayResponse

##########################################
# Serializer需要自己重写create update方法#
# ModelSerializer  已经简单的实现了   ####
##########################################
class ShopCartSerializer(serializers.Serializer):
    """
    因为继承的是Serializer 所以需要重写里面的创建更新操作
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

    # 此时已经处理过的数据为validated_data  在serializer里面user不是直接放在request，而是在context上下文
    # initial_data 是前端传过来未处理的数据
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
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay_client_config = AlipayClientConfig()
        alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
        alipay_client_config.app_id = '2016101100658599'
        alipay_client_config.app_private_key = 'MIIEpQIBAAKCAQEAlYeeYtr26BOVeuk5ZbJnkzLp5X763iW8yiJ08/gXjdvw0OAQw0ltUc/FogSRKscY1Ax0CiPfyxrp7bRR8mBM0aT4EwvfoOzqT9Dy4x+nhbsEgeX2V+5MSLIW05yRZWSY+2YGLagKbB9BKzXmXvKSYdaoNtKHWao/FE7adMWBec6k97Ez6G22cvwj18WDiZC6N/xIXslh9Lw4KeQr5NVPxC9S1lBt8qByxUyPMSlqcbxp+LOBsym8OZDC15luN9hoKU9tQNiyErvNsjcSmh0dSOz+IneoDxFviLypDLgsUUrmsh0bKaxL15boh9AdIt5H0SH6+gZtGv8zf6397+U6YwIDAQABAoIBAAIdc/kT/dAUjtW5PM2ac2qamsJbRHMl94Coch0NUk/4X3Sk5rfMbxZsKPB8vgzr2gcN0gperYiy7cIl/c6+2/dPLQ8f6N7e2wWcAAOEbBsxJQQtW4ms3jldA4OkwE292YgczlOQ/+y9mG9jCMopBjcKEUENQ0raZKAF6YMjVAyEARAn3D2vOGYxECy+hwy4rYWRRHtmKQGrNb1wkH5JNptMjCIyP0NA/DZQ7tCHK0Cj1jGOR9PjR/qWsy+mzzafoFcU46r6pPYc4+gYYy1nTCUHnR1sQsnr08/XOP0oktAL66tbBf+NWVEG453CbgEPBccZ+x4z+YX7ow539cIUbeECgYEA+Z+viU1sQDkxHZGKulyB5VoVTWEYD7HWlaNWc0KXf829ncW75Kyz9zZfswCLYLR2vHcMkVaQhXcRfi7gSByANZ7ZYdBHcIU/4O0wNyNygZ4xU1sp5nKnlHQkFj+dOpVD3/6wVof1EXy2AlWX8zYHYiZ2n7L8dob34A6onR5CKrMCgYEAmVlokH78d8TZj0198xViKiHlT0/Plj5rLulVreejeACemhJogAWClbXS3XGE99d7kymz0AEo2o7xqRWIB5wURa0xoFN8Ahpd0W8PV8sKSLqKeIHiRZClBxTc1PlpYa8fIWl/ubPYrfZMszQjyxFI/woC1quJEntn+I5KFE/KSZECgYEAsV17Nk3iysdYVLAjKEOusC4P0MladVxhIjXKqV75kn+3aTEkTllADjl+Sgvq/K19aHAWZ/Zf/dUagtP/3H0TxAW4Y72/5P1o5ALkLWlsZRjn51hxLyLsW5kiQwS0TPneHnwzA2jbAq/gC0ySCOes21qFEvf0VquT2InR2MG1Ne0CgYEAkDDgwFWXISsIgtWTo1ks937ttljOUXCZqf+fH6laLQEwIKFEf3Qu6ISSJMSUCdMlECg7Ok+M0Y1tL9beFIGvEiEbM6ysQvH123L5U0zIe8BjaZJ/Z3ftpK36Q4vNiht3QxyHC99O06xvTGWvbkbvg1gveRjMB4PgLHfmshiglfECgYEA8Xyk50ihs2gEcrCQRy/W1/FbPiS9nzljvy8hvBJOb9yK5Oq2fHWYaK6qvHvVVFU9CXMBJDyBE5XfwQxypZEtjB+C9qylGrY8JTYU943G4L8LfANNyMSEjuFfLgMdjy5joNktw6RTTLNP5I2+WXrnxjyqYBHrL9w/H5GZyylK2gk='
        alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgUnmcN1BEo9ZdwUXDj6YxnSGzhlQ4Sog5Wk8o3c7fn+7rvuGjXDA/QyzhAyUW/kSCzksK3u0sOzQYpmCH8leQge4tknFS83QZcpwElvJ/Msv00xKWCCNNo9+e4lmh7AfmeNZS8//zDYRRsZHaODLjkXcRu+/oqZoP3w2HzUa7eiaR8F8Hh6zQjfu6BXR1EuB2Djk9oLjoxPh+0jvxdf5VI7sxmVVHt4htUecSMYkO7QBNVWw1snAMHn9nF8My3gZGdIRUpxgnJHNle6hQr2i0RBYu7iQNz/n+oo+jkxaH7R9FBTABhimDyM2eXenwhYTvAbFAMafcov8aas9TDxY7QIDAQAB'

        client = DefaultAlipayClient(alipay_client_config=alipay_client_config)

        # 对照接口文档，构造请求对象
        model = AlipayTradePagePayModel()
        goods_list = list()
        goods1 = GoodsDetail()
        goods1.goods_id = "apple-01"
        goods1.goods_name = "ipad"
        goods1.price = 1
        goods1.quantity = 1
        goods_list.append(goods1)
        model.goods_detail = goods_list
        model.out_trade_no = obj.order_sn
        model.product_code = "FAST_INSTANT_TRADE_PAY"
        model.subject = obj.order_sn
        model.timeout_express = "90m"
        model.total_amount = obj.order_mount
        # 实例化一个请求对象
        request = AlipayTradePagePayRequest(biz_model=model)
        # get请求 用户支付成功后返回的页面请求地址
        request.return_url = "http://111.229.129.33:8000/alipay/return/"
        # post请求 用户支付成功后通知商家的请求地址
        request.notify_url = "http://111.229.129.33:8000/alipay/return/"
        response_content = None
        try:
            # 向阿里支付发送一个请求，返回一个支付页面url
            response_content = client.page_execute(request, http_method="GET")
        except Exception as e:
            print(e)
        if not response_content:
            print("failed execute")
        else:
            response = AlipayTradePagePayResponse()
            # 解析响应结果
            # response.parse_response_content(response_content)
            # print('222',response)
            if response.is_success():
                # 如果业务成功，则通过respnse属性获取需要的值
                print("调用成功")
                print("response_url:", response_content)
            else:
                # 如果业务失败，则从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
                print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)
        return response_content
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
    goods = GoodsSerializer(many=False)  # order是一个外键 所以只有一个

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    """订单详情信息"""
    goods = OrderGoodsSerializer(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay_client_config = AlipayClientConfig()
        alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
        alipay_client_config.app_id = '2016101100658599'
        alipay_client_config.app_private_key = 'MIIEpQIBAAKCAQEAlYeeYtr26BOVeuk5ZbJnkzLp5X763iW8yiJ08/gXjdvw0OAQw0ltUc/FogSRKscY1Ax0CiPfyxrp7bRR8mBM0aT4EwvfoOzqT9Dy4x+nhbsEgeX2V+5MSLIW05yRZWSY+2YGLagKbB9BKzXmXvKSYdaoNtKHWao/FE7adMWBec6k97Ez6G22cvwj18WDiZC6N/xIXslh9Lw4KeQr5NVPxC9S1lBt8qByxUyPMSlqcbxp+LOBsym8OZDC15luN9hoKU9tQNiyErvNsjcSmh0dSOz+IneoDxFviLypDLgsUUrmsh0bKaxL15boh9AdIt5H0SH6+gZtGv8zf6397+U6YwIDAQABAoIBAAIdc/kT/dAUjtW5PM2ac2qamsJbRHMl94Coch0NUk/4X3Sk5rfMbxZsKPB8vgzr2gcN0gperYiy7cIl/c6+2/dPLQ8f6N7e2wWcAAOEbBsxJQQtW4ms3jldA4OkwE292YgczlOQ/+y9mG9jCMopBjcKEUENQ0raZKAF6YMjVAyEARAn3D2vOGYxECy+hwy4rYWRRHtmKQGrNb1wkH5JNptMjCIyP0NA/DZQ7tCHK0Cj1jGOR9PjR/qWsy+mzzafoFcU46r6pPYc4+gYYy1nTCUHnR1sQsnr08/XOP0oktAL66tbBf+NWVEG453CbgEPBccZ+x4z+YX7ow539cIUbeECgYEA+Z+viU1sQDkxHZGKulyB5VoVTWEYD7HWlaNWc0KXf829ncW75Kyz9zZfswCLYLR2vHcMkVaQhXcRfi7gSByANZ7ZYdBHcIU/4O0wNyNygZ4xU1sp5nKnlHQkFj+dOpVD3/6wVof1EXy2AlWX8zYHYiZ2n7L8dob34A6onR5CKrMCgYEAmVlokH78d8TZj0198xViKiHlT0/Plj5rLulVreejeACemhJogAWClbXS3XGE99d7kymz0AEo2o7xqRWIB5wURa0xoFN8Ahpd0W8PV8sKSLqKeIHiRZClBxTc1PlpYa8fIWl/ubPYrfZMszQjyxFI/woC1quJEntn+I5KFE/KSZECgYEAsV17Nk3iysdYVLAjKEOusC4P0MladVxhIjXKqV75kn+3aTEkTllADjl+Sgvq/K19aHAWZ/Zf/dUagtP/3H0TxAW4Y72/5P1o5ALkLWlsZRjn51hxLyLsW5kiQwS0TPneHnwzA2jbAq/gC0ySCOes21qFEvf0VquT2InR2MG1Ne0CgYEAkDDgwFWXISsIgtWTo1ks937ttljOUXCZqf+fH6laLQEwIKFEf3Qu6ISSJMSUCdMlECg7Ok+M0Y1tL9beFIGvEiEbM6ysQvH123L5U0zIe8BjaZJ/Z3ftpK36Q4vNiht3QxyHC99O06xvTGWvbkbvg1gveRjMB4PgLHfmshiglfECgYEA8Xyk50ihs2gEcrCQRy/W1/FbPiS9nzljvy8hvBJOb9yK5Oq2fHWYaK6qvHvVVFU9CXMBJDyBE5XfwQxypZEtjB+C9qylGrY8JTYU943G4L8LfANNyMSEjuFfLgMdjy5joNktw6RTTLNP5I2+WXrnxjyqYBHrL9w/H5GZyylK2gk='
        alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgUnmcN1BEo9ZdwUXDj6YxnSGzhlQ4Sog5Wk8o3c7fn+7rvuGjXDA/QyzhAyUW/kSCzksK3u0sOzQYpmCH8leQge4tknFS83QZcpwElvJ/Msv00xKWCCNNo9+e4lmh7AfmeNZS8//zDYRRsZHaODLjkXcRu+/oqZoP3w2HzUa7eiaR8F8Hh6zQjfu6BXR1EuB2Djk9oLjoxPh+0jvxdf5VI7sxmVVHt4htUecSMYkO7QBNVWw1snAMHn9nF8My3gZGdIRUpxgnJHNle6hQr2i0RBYu7iQNz/n+oo+jkxaH7R9FBTABhimDyM2eXenwhYTvAbFAMafcov8aas9TDxY7QIDAQAB'

        client = DefaultAlipayClient(alipay_client_config=alipay_client_config)

        # 对照接口文档，构造请求对象
        model = AlipayTradePagePayModel()
        goods_list = list()
        goods1 = GoodsDetail()
        goods1.goods_id = "apple-01"
        goods1.goods_name = "ipad"
        goods1.price = 1
        goods1.quantity = 1
        goods_list.append(goods1)
        model.goods_detail = goods_list
        model.out_trade_no = obj.order_sn
        model.product_code = "FAST_INSTANT_TRADE_PAY"
        model.subject = obj.order_sn
        model.timeout_express = "90m"
        model.total_amount = obj.order_mount
        # 实例化一个请求对象
        request = AlipayTradePagePayRequest(biz_model=model)
        # get请求 用户支付成功后返回的页面请求地址
        request.return_url = "http://111.229.129.33:8000/alipay/return/"
        # post请求 用户支付成功后通知商家的请求地址
        request.notify_url = "http://111.229.129.33:8000/alipay/return/"
        response_content = None
        try:
            # 向阿里支付发送一个请求，返回一个支付页面url
            response_content = client.page_execute(request, http_method="GET")
        except Exception as e:
            print(e)
        if not response_content:
            print("failed execute")
        else:
            response = AlipayTradePagePayResponse()
            # 解析响应结果
            # response.parse_response_content(response_content)
            # print('222',response)
            if response.is_success():
                # 如果业务成功，则通过respnse属性获取需要的值
                print("调用成功")
                print("response_url:", response_content)
            else:
                # 如果业务失败，则从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
                print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)
        return response_content
    class Meta:
        model = OrderInfo
        fields = "__all__"

