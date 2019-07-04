from random import choice
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import mixins, viewsets, status, permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.shortcuts import render
from rest_framework_jwt.serializers import jwt_decode_handler, jwt_payload_handler, jwt_encode_handler

from users.serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from ucode.yunpian import YunPian
from online.settings import APIKEY
from .models import VerifyCode
# Create your views here.

User = get_user_model()

class CustomBackend(ModelBackend):
#     """
#     自定义 用户验证 需要继承modelbackend  重写认证方法
#     """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 用户名和手机都能登录
            user = User.objects.get(
                Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def get_code(self):
        """
        生成四位验证码
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    # 重写create方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # 验证不通过 直接抛出400异常

        mobile = serializer.validated_data["mobile"]
        code = self.get_code()
        yunpian = YunPian(APIKEY)
        sms_status = yunpian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            return Response({
                "mobile":sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 在发送成功后保存到数据库
            code_ver = VerifyCode(mobile=mobile, code=code)
            code_ver.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户 注册  详情 个人中心
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    # 用浏览器调试 徐娅提供session验证  JWT
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)

    def get_serializer_class(self):
        """
        重写 获取serializer_class方法  从而让程序能够 动态 选择serializers
        :return:
        """
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
        return UserDetailSerializer

    def get_permissions(self):
        """
        用户需要先权限验证  但是注册时候，是不能走验证的  所以要用动态方式判断，
        那么找到rest permissions 源码可知  只要重写 get_permissions方法,返回一个permission()实例
        action 放到self里面 只有在使用ViewSet时候才会显示出来
        :return:
        """
        if self.action == "retrieve":
            return [permissions.IsAuthenticated(),]
        elif self.action == "create":
            return [permissions.AllowAny(), ]
        return []

    # 获取user.id  由于创建时候没有给id  所以 重写 get_object 返回user详情实例
    def get_object(self):
        return self.request.user

    # 如果想要在 注册时就登录  那么我们需要在此传递一个token接口  保存的时候保存token
    # 为什么要重xie它？  serializer 返回的是serializers 存放的fields 并没有 token值
    def create(self, request, *args, **kwargs):
        # 注册功能实现
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username
        print(re_dict)
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 真正的存入数据库操作
    def perform_create(self, serializer):
        return serializer.save()