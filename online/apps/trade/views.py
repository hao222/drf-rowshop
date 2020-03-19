from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets, mixins
# Create your views here.
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.views import APIView

from trade.serializers import ShopCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from ucode.permissions import IsOwnerOrReadOnly
from trade.models import ShoppingCart, OrderInfo, OrderGoods

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient

from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.GoodsDetail import GoodsDetail

from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.response.AlipayTradePagePayResponse import AlipayTradePagePayResponse
from online.settings import private_key, ali_pub_key, app_id, test_box


class ReadOnlyModelViewset(viewsets.ModelViewSet):
    """
    购物车功能
    list create delete update
    """
    serializer_class = ShopCartSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # 查询的时候 用商品id 查询  而不是购物车id
    lookup_field = "goods_id"
    # 增加商品到购物车，商品的库存量 -1
    def perform_create(self, serializer):
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()
    # 删除
    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()
    # 修改
    def perform_update(self, serializer):
        # serializer.instance.id 取出序列化之后的实例 id
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        nums = saved_record - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)



class OrderViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create：
        新增订单
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer
    pagination_class = None

    # 动态配置serializer  详情信息
    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    # 获取订单列表
    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    # 在订单保存之前还需要两步操作，所以需要重新定义perform_create方法
    # 将购物车的商品保存到Order_goods  然后清空购物车
    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            # 清空购物车
            shop_cart.delete()

        return order


def ali_pay():
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '2016101100658599'
    alipay_client_config.app_private_key = 'MIIEpQIBAAKCAQEAlYeeYtr26BOVeuk5ZbJnkzLp5X763iW8yiJ08/gXjdvw0OAQw0ltUc/FogSRKscY1Ax0CiPfyxrp7bRR8mBM0aT4EwvfoOzqT9Dy4x+nhbsEgeX2V+5MSLIW05yRZWSY+2YGLagKbB9BKzXmXvKSYdaoNtKHWao/FE7adMWBec6k97Ez6G22cvwj18WDiZC6N/xIXslh9Lw4KeQr5NVPxC9S1lBt8qByxUyPMSlqcbxp+LOBsym8OZDC15luN9hoKU9tQNiyErvNsjcSmh0dSOz+IneoDxFviLypDLgsUUrmsh0bKaxL15boh9AdIt5H0SH6+gZtGv8zf6397+U6YwIDAQABAoIBAAIdc/kT/dAUjtW5PM2ac2qamsJbRHMl94Coch0NUk/4X3Sk5rfMbxZsKPB8vgzr2gcN0gperYiy7cIl/c6+2/dPLQ8f6N7e2wWcAAOEbBsxJQQtW4ms3jldA4OkwE292YgczlOQ/+y9mG9jCMopBjcKEUENQ0raZKAF6YMjVAyEARAn3D2vOGYxECy+hwy4rYWRRHtmKQGrNb1wkH5JNptMjCIyP0NA/DZQ7tCHK0Cj1jGOR9PjR/qWsy+mzzafoFcU46r6pPYc4+gYYy1nTCUHnR1sQsnr08/XOP0oktAL66tbBf+NWVEG453CbgEPBccZ+x4z+YX7ow539cIUbeECgYEA+Z+viU1sQDkxHZGKulyB5VoVTWEYD7HWlaNWc0KXf829ncW75Kyz9zZfswCLYLR2vHcMkVaQhXcRfi7gSByANZ7ZYdBHcIU/4O0wNyNygZ4xU1sp5nKnlHQkFj+dOpVD3/6wVof1EXy2AlWX8zYHYiZ2n7L8dob34A6onR5CKrMCgYEAmVlokH78d8TZj0198xViKiHlT0/Plj5rLulVreejeACemhJogAWClbXS3XGE99d7kymz0AEo2o7xqRWIB5wURa0xoFN8Ahpd0W8PV8sKSLqKeIHiRZClBxTc1PlpYa8fIWl/ubPYrfZMszQjyxFI/woC1quJEntn+I5KFE/KSZECgYEAsV17Nk3iysdYVLAjKEOusC4P0MladVxhIjXKqV75kn+3aTEkTllADjl+Sgvq/K19aHAWZ/Zf/dUagtP/3H0TxAW4Y72/5P1o5ALkLWlsZRjn51hxLyLsW5kiQwS0TPneHnwzA2jbAq/gC0ySCOes21qFEvf0VquT2InR2MG1Ne0CgYEAkDDgwFWXISsIgtWTo1ks937ttljOUXCZqf+fH6laLQEwIKFEf3Qu6ISSJMSUCdMlECg7Ok+M0Y1tL9beFIGvEiEbM6ysQvH123L5U0zIe8BjaZJ/Z3ftpK36Q4vNiht3QxyHC99O06xvTGWvbkbvg1gveRjMB4PgLHfmshiglfECgYEA8Xyk50ihs2gEcrCQRy/W1/FbPiS9nzljvy8hvBJOb9yK5Oq2fHWYaK6qvHvVVFU9CXMBJDyBE5XfwQxypZEtjB+C9qylGrY8JTYU943G4L8LfANNyMSEjuFfLgMdjy5joNktw6RTTLNP5I2+WXrnxjyqYBHrL9w/H5GZyylK2gk='
    alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgUnmcN1BEo9ZdwUXDj6YxnSGzhlQ4Sog5Wk8o3c7fn+7rvuGjXDA/QyzhAyUW/kSCzksK3u0sOzQYpmCH8leQge4tknFS83QZcpwElvJ/Msv00xKWCCNNo9+e4lmh7AfmeNZS8//zDYRRsZHaODLjkXcRu+/oqZoP3w2HzUa7eiaR8F8Hh6zQjfu6BXR1EuB2Djk9oLjoxPh+0jvxdf5VI7sxmVVHt4htUecSMYkO7QBNVWw1snAMHn9nF8My3gZGdIRUpxgnJHNle6hQr2i0RBYu7iQNz/n+oo+jkxaH7R9FBTABhimDyM2eXenwhYTvAbFAMafcov8aas9TDxY7QIDAQAB'

    alipay_client = DefaultAlipayClient(alipay_client_config=alipay_client_config)
    return alipay_client


class AlipayView(APIView):
    """
    阿里支付  支付返回 get请求 return_url   post请求的notify_url
    """
    def get(self, request):
        return render(request, "pay.html")

    def post(self, request):
        client = ali_pay()
        # 对照接口文档，构造请求对象
        model = AlipayTradePagePayModel()

        model.out_trade_no = "11111111122222"
        model.product_code = "FAST_INSTANT_TRADE_PAY"
        # model.store_id = "NJ_001"
        model.subject = "111111112122"
        model.timeout_express = "90m"
        model.total_amount = 1
        # 实例化一个请求对象
        request = AlipayTradePagePayRequest(biz_model=model)
        # get请求 用户支付成功后返回的页面请求地址
        request.return_url = "http://111.229.129.33:8000/alipay/handler"
        # post请求 用户支付成功后通知商家的请求地址
        request.notify_url = "http://111.229.129.33:8000/alipay/handler"
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
        return redirect(response_content)


class PayHandlerView(APIView):
    def get(self,request):
        print('1111',request.GET)
        query_dict = {}
        if request.GET:
            for k, v in request.GET.items():
                query_dict[k] = v
            order_sn = query_dict.get("out_trade_no", None)
            trade_no = query_dict.get("trade_no", None)
            trade_status = query_dict.get("trade_status", None)

            existed_order = OrderInfo.objects.filter(order_sn=order_sn)
            for order in existed_order:
                order.pay_status = trade_status
                order.trade_no = trade_no
                order.pay_time = datetime.now()
                order.save()
            return Response("success")
        else:
            pass
    def post(self, request):
        print(request.data)
        query_dict = {}
        if request.data:
            for k, v in request.data.items():
                query_dict[k] = v
            order_sn = query_dict.get("out_trade_no", None)
            trade_no = query_dict.get("trade_no", None)
            trade_status = query_dict.get("trade_status", None)

            existed_order = OrderInfo.objects.filter(order_sn=order_sn)
            for order in existed_order:
                order.pay_status = trade_status
                order.trade_no = trade_no
                order.pay_time = datetime.now()
                order.save()
            return Response("success")
        else:
            pass


class AlipayView1(APIView):
    def get(self,request):
        print('get', request.GET)
        # query_dict = {}
        # if request.query_params:
        #     for k, v in request.GET.items():
        #         query_dict[k] = v
        #     order_sn = query_dict.get("out_trade_no", None)
        #     trade_no = query_dict.get("trade_no", None)
        #     trade_status = query_dict.get("trade_status", None)
        #
        #     existed_order = OrderInfo.objects.filter(order_sn=order_sn)
        #     for order in existed_order:
        #         order.pay_status = trade_status
        #         order.trade_no = trade_no
        #         order.pay_time = datetime.now()
        #         order.save()
            # vue 路由跳转前beforeach 判断是否有nextPath
        response = redirect("index")
        response.set_cookie("nextPath", "pay", max_age=2)
        return response
            # return Response("success")
        # else:
        #     # return redirect("index")
        #     return Response("failed")
    def post(self, request):
        print('post', request.POST)
        query_dict = {}
        if request.POST:
            for k, v in request.POST.items():
                query_dict[k] = v
            order_sn = query_dict.get("out_trade_no", None)
            trade_no = query_dict.get("trade_no", None)
            trade_status = query_dict.get("trade_status", None)

            existed_order = OrderInfo.objects.filter(order_sn=order_sn)
            for order in existed_order:

                # 售卖数量
                order_goods = order.goods.all()
                for good in order_goods:
                    goods = good.goods
                    goods.sold_num += good.goods_num

                order.pay_status = trade_status
                order.trade_no = trade_no
                order.pay_time = datetime.now()
                order.save()
            return Response("success")
        else:
            return Response("failed")