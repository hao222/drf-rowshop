from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from user_operation.serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, \
    AddressSerializer
from .models import UserFav, UserLeavingMessage, UserAddress
from ucode.permissions import IsOwnerOrReadOnly
# Create your views here.

class UserFavViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    用户收藏  添加  删除  展示
    list
        展示
    retitve：
        判断某商品是否收藏
    create：
        收藏
    """
    # RetrieveModelMixin   切记不要忘了RetrieveModelMixin  它可以返回现有模型实例详情！！！！
    # lookup_field 获取不是所有用户的商品id  而是已经筛选过后的queryset的
    lookup_field = "goods_id"
    # 权限  isauthenticated 判断是否提供认证信息   IsOwnerOrReadOnly 判断是否为当前用户
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    # 如果只配置jwt 认证模式的话，在后端restframework无法登进去  则需要加入 sessionauth
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 获取list 的时候  只需要获取当前用户的数据
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    # 新建收藏的时候，goods 的收藏数 +1  相当于更新   或者使用信号量来完成
    def perform_create(self, serializer):
        instance = serializer.save()
        goods = instance.goods
        goods.fav_num +=1
        goods.save()
    # 删除操作的时候，调用此函数，商品的收藏数-1 并删除userfav
    def perform_destroy(self, instance):
        goods = instance.goods
        goods.fav_num -=1
        goods.save()
        instance.delete()

    def get_serializer_class(self):
        # 动态选择序列化类
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer
        return UserFavSerializer


class LeavingMessageViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    """
    list  展示留言列表
    create 添加留言
    delete 删除留言

    """
    serializer_class = LeavingMessageSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


# ModelViewSet 增删改查包完
class AddressViewSet(viewsets.ModelViewSet):
    """
    收获地址管理
    list 获取收获地址
    create 添加收获地址
    update：更新收获地址
    delete ：删除
    """
    serializer_class = AddressSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
