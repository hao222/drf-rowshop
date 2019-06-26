from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from online.settings import REGEX_PHONE
import re
from datetime import datetime, timedelta
from .models import VerifyCode

User = get_user_model()

# 发送验证码 只需要一个手机号  所以用Serializer
class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号
        :param data:
        :return:
        """

        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机是否合法
        if not re.match(REGEX_PHONE, mobile):
            raise serializers.ValidationError("格式不合法")

        # 手机号之前发送时间   发送频率
        one_minute_age = datetime.now() - timedelta(minutes=1) # 1分钟之前
        if VerifyCode.objects.filter(add_time__gt=one_minute_age, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送不到1分钟")


class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册
    """
    # 自定义字段     error_message 可以自定义提示消息
    code = serializers.CharField(required=True, max_length=4, min_length=4, help_text="验证码", error_messages={
        "required": "请输入验证码",
        "blank": "请输入验证码",
        "max_length": "不能为空"
    })
    # 验证username 是否存在  UniqueValidator 唯一性判断
    username = serializers.CharField(required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    # 验证字段  self.initial_data 前端post传过来的值
    def validate_code(self, code):
        ver_recode = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if ver_recode:
            last_codes = ver_recode[0]  # 最新的一条
            five_minute_age = datetime.now() - timedelta(minutes=5) # 有效期五分钟
            if five_minute_age < last_codes.add_time:
                raise serializers.ValidationError("失效")
            if last_codes.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    # 作用所有的字段之上  attrs 每个字段validate后 所有字段的组合为data
    # 在这里面 做字段统一的处理  上面的为单个字段的处理
    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        # 继承自django USer  搜哦一username必填
        fields = ("username", "mobile", "code")
