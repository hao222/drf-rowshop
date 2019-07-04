"""online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin

from django.urls import path, re_path, include
from django.views.generic import TemplateView

import xadmin
from online.settings import MEDIA_ROOT
from django.views.static import serve

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as vs
# from goods.views_base import GoodsListView
from goods.views import GoodsListViewSet, CategoryViewSet, BannerViewset, IndexCategoryViewset
from goods import views
from trade.views import ReadOnlyModelViewset, OrderViewset
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewset, LeavingMessageViewSet, AddressViewSet


router = DefaultRouter()
#配置goods的url
router.register(r'goods', GoodsListViewSet, base_name="goods")
#配置goodscategory的url
router.register(r'categorys', CategoryViewSet, base_name="categorys")
# 配置短信
router.register(r'code', SmsCodeViewSet, base_name="code")
# 用户注册
router.register(r'users', UserViewSet, base_name="users")
# 用户收藏
router.register(r'userfavs', UserFavViewset, base_name="userfavs")
# 用户留言
router.register(r'lvmessage', LeavingMessageViewSet, base_name="lvmessage")
# 收货地址
router.register(r'address', AddressViewSet, base_name="address")
# 购物车
router.register(r'shopcarts', ReadOnlyModelViewset, base_name="shopcarts")
# 订单相关
router.register(r'orders', OrderViewset, base_name="orders")
# 轮播图
router.register(r'banners', BannerViewset, base_name="banners")
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('docs/', include_docs_urls(title="online商品")),
    # 首页
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),
]

# drf 自带的认证模式该路由返回一个json格式的{ 'token' : '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'}  保存到我们的数据库的那个token表
# urlpatterns += [
#     path(r'api-token-auth/', vs.obtain_auth_token)
# ]
from rest_framework_jwt.views import obtain_jwt_token
# jwt的认证接口
urlpatterns += [
    path(r'^login/$', obtain_jwt_token),
]

# 第三方登录  url 集成
urlpatterns += [
    path('', include('social_django.urls', namespace='social'))
]