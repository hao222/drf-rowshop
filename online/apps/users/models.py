from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.

class UserApp(AbstractUser):
    """
    user to app
    """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    gender = models.CharField(max_length=6, choices=(("male", u"男"),("female", u"女")), default="female", verbose_name="性别")
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    #此处应该返回username 因为继承的AbstractUser里的username就是不为空  而此处的name可以为空 所以后面会报错no——string
    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    code for phone
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
