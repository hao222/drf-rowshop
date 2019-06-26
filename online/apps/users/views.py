from random import choice

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import mixins, viewsets, status
from django.shortcuts import render

from users.serializers import SmsSerializer, UserRegSerializer
from ucode.yunpian import YunPian
from online.settings import APIKEY
from .models import VerifyCode
# Create your views here.

User = get_user_model()

class CustomBackend(ModelBackend):
    """
    自定义 用户验证 需要继承modelbackend  重写认证方法
    """
    def authenticate(self,username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
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


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    注册 用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
