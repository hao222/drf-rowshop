#!/usr/bin/env python
# encoding: utf-8
from goods.models import Goods

__author__ = 'hao'

from django.views.generic.base import View

# from django.views.generic import ListView

class GoodsListView(View):
    def get(self, request):
        """
        通过django的view实现商品列表页
        :param request:
        :return:
        """
        json_list = []
        goods = Goods.objects.all()[:10]
        # for good in goods:
        #     json_dict = {}
        #     json_dict["name"] = good.name
        #     json_dict["category"] = good.category.name
        #     json_dict["market_price"] = good.market_price
        #     json_list.append(json_dict)

        # 直接将model里的数据 转化成 字典格式   但是有些数据是不能序列化的 date 和image
        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)

        # 所以我们需要 用到serializers
        import json
        from django.core import serializers
        json_data = serializers.serialize("json", goods) # 已经序列化的数据
        json_data = json.loads(json_data)   #反序列化

        from django.http import HttpResponse,JsonResponse
        import json
        # return HttpResponse(json_data, content_type="application/json")
        return JsonResponse(json_data, safe=False)