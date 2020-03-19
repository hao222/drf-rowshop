#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import traceback

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient

from alipay.aop.api.domain.AlipayTradePayModel import AlipayTradePayModel
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.GoodsDetail import GoodsDetail

from alipay.aop.api.request.AlipayTradePayRequest import AlipayTradePayRequest
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.response.AlipayTradePagePayResponse import AlipayTradePagePayResponse
from alipay.aop.api.response.AlipayTradePayResponse import AlipayTradePayResponse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')


if __name__ == '__main__':
    """
    设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
    """
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '2016101100658599'
    alipay_client_config.app_private_key = 'MIIEpQIBAAKCAQEAlYeeYtr26BOVeuk5ZbJnkzLp5X763iW8yiJ08/gXjdvw0OAQw0ltUc/FogSRKscY1Ax0CiPfyxrp7bRR8mBM0aT4EwvfoOzqT9Dy4x+nhbsEgeX2V+5MSLIW05yRZWSY+2YGLagKbB9BKzXmXvKSYdaoNtKHWao/FE7adMWBec6k97Ez6G22cvwj18WDiZC6N/xIXslh9Lw4KeQr5NVPxC9S1lBt8qByxUyPMSlqcbxp+LOBsym8OZDC15luN9hoKU9tQNiyErvNsjcSmh0dSOz+IneoDxFviLypDLgsUUrmsh0bKaxL15boh9AdIt5H0SH6+gZtGv8zf6397+U6YwIDAQABAoIBAAIdc/kT/dAUjtW5PM2ac2qamsJbRHMl94Coch0NUk/4X3Sk5rfMbxZsKPB8vgzr2gcN0gperYiy7cIl/c6+2/dPLQ8f6N7e2wWcAAOEbBsxJQQtW4ms3jldA4OkwE292YgczlOQ/+y9mG9jCMopBjcKEUENQ0raZKAF6YMjVAyEARAn3D2vOGYxECy+hwy4rYWRRHtmKQGrNb1wkH5JNptMjCIyP0NA/DZQ7tCHK0Cj1jGOR9PjR/qWsy+mzzafoFcU46r6pPYc4+gYYy1nTCUHnR1sQsnr08/XOP0oktAL66tbBf+NWVEG453CbgEPBccZ+x4z+YX7ow539cIUbeECgYEA+Z+viU1sQDkxHZGKulyB5VoVTWEYD7HWlaNWc0KXf829ncW75Kyz9zZfswCLYLR2vHcMkVaQhXcRfi7gSByANZ7ZYdBHcIU/4O0wNyNygZ4xU1sp5nKnlHQkFj+dOpVD3/6wVof1EXy2AlWX8zYHYiZ2n7L8dob34A6onR5CKrMCgYEAmVlokH78d8TZj0198xViKiHlT0/Plj5rLulVreejeACemhJogAWClbXS3XGE99d7kymz0AEo2o7xqRWIB5wURa0xoFN8Ahpd0W8PV8sKSLqKeIHiRZClBxTc1PlpYa8fIWl/ubPYrfZMszQjyxFI/woC1quJEntn+I5KFE/KSZECgYEAsV17Nk3iysdYVLAjKEOusC4P0MladVxhIjXKqV75kn+3aTEkTllADjl+Sgvq/K19aHAWZ/Zf/dUagtP/3H0TxAW4Y72/5P1o5ALkLWlsZRjn51hxLyLsW5kiQwS0TPneHnwzA2jbAq/gC0ySCOes21qFEvf0VquT2InR2MG1Ne0CgYEAkDDgwFWXISsIgtWTo1ks937ttljOUXCZqf+fH6laLQEwIKFEf3Qu6ISSJMSUCdMlECg7Ok+M0Y1tL9beFIGvEiEbM6ysQvH123L5U0zIe8BjaZJ/Z3ftpK36Q4vNiht3QxyHC99O06xvTGWvbkbvg1gveRjMB4PgLHfmshiglfECgYEA8Xyk50ihs2gEcrCQRy/W1/FbPiS9nzljvy8hvBJOb9yK5Oq2fHWYaK6qvHvVVFU9CXMBJDyBE5XfwQxypZEtjB+C9qylGrY8JTYU943G4L8LfANNyMSEjuFfLgMdjy5joNktw6RTTLNP5I2+WXrnxjyqYBHrL9w/H5GZyylK2gk='
    alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgUnmcN1BEo9ZdwUXDj6YxnSGzhlQ4Sog5Wk8o3c7fn+7rvuGjXDA/QyzhAyUW/kSCzksK3u0sOzQYpmCH8leQge4tknFS83QZcpwElvJ/Msv00xKWCCNNo9+e4lmh7AfmeNZS8//zDYRRsZHaODLjkXcRu+/oqZoP3w2HzUa7eiaR8F8Hh6zQjfu6BXR1EuB2Djk9oLjoxPh+0jvxdf5VI7sxmVVHt4htUecSMYkO7QBNVWw1snAMHn9nF8My3gZGdIRUpxgnJHNle6hQr2i0RBYu7iQNz/n+oo+jkxaH7R9FBTABhimDyM2eXenwhYTvAbFAMafcov8aas9TDxY7QIDAQAB'

    """
    得到客户端对象。
    注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
    logger参数用于打印日志，不传则不打印，建议传递。
    """
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)

    """
    系统接口示例：alipay.trade.pay
    """
    # 对照接口文档，构造请求对象
    model = AlipayTradePagePayModel()
    # model.auth_code = "282877775259787048"
    goods_list = list()
    goods1 = GoodsDetail()
    goods1.goods_id = "apple-01"
    goods1.goods_name = "ipad"
    goods1.price = 1
    goods1.quantity = 1
    goods_list.append(goods1)
    model.goods_detail = goods_list
    # model.operator_id = "yx_001"
    model.out_trade_no = "20180510AB019"
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    # model.scene = "bar_code"
    model.store_id = "NJ_001"
    model.subject = "huabeitest"
    model.timeout_express = "90m"
    model.total_amount = 1
    # 实例化一个请求对象
    request = AlipayTradePagePayRequest(biz_model=model)
    # get请求 用户支付成功后返回的页面请求地址
    request.return_url = "http://111.229.129.33:8000/alipay/return"
    # post请求 用户支付成功后通知商家的请求地址
    request.notify_url = "http://111.229.129.33:8000/alipay/return"

    # 如果有auth_token、app_auth_token等其他公共参数，放在udf_params中
    # udf_params = dict()
    # from alipay.aop.api.constant.ParamConstants import *
    # udf_params[P_APP_AUTH_TOKEN] = "xxxxxxx"
    # request.udf_params = udf_params
    # 执行请求，执行过程中如果发生异常，会抛出，请打印异常栈
    response_content = None
    try:
        # 向阿里支付发送一个请求，返回一个支付页面url
        response_content = client.page_execute(request,http_method="GET")
    except Exception as e:
        print(traceback.format_exc())
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

