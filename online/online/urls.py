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
from goods.views import GoodsListViewSet, CategoryViewSet, BannerViewset, IndexCategoryViewset, HotSearchsViewset
from goods import views
from trade.views import ReadOnlyModelViewset, OrderViewset, AlipayView, PayHandlerView, AlipayView1
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
router.register(r'messages', LeavingMessageViewSet, base_name="messages")
# 收货地址
router.register(r'address', AddressViewSet, base_name="address")
# 购物车
router.register(r'shopcarts', ReadOnlyModelViewset, base_name="shopcarts")
# 订单相关
router.register(r'orders', OrderViewset, base_name="orders")
# 轮播图
router.register(r'banners', BannerViewset, base_name="banners")
# 首页商品展示
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")
# 热搜商品hotsearchs
router.register(r'hotsearchs', HotSearchsViewset, base_name="hotsearchs")


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    path('api-auth/', include('rest_framework.urls', namespace="rest_framework")),
    path('', include(router.urls)),
    # apidoc 查看页面
    path('docs/', include_docs_urls(title="生鲜")),
    # 首页
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),
    path('test/', include("goods.urls"))
]

# drf 自带的认证模式该路由返回一个json格式的{ 'token' : '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'}  保存到我们的数据库的那个token表
# urlpatterns += [p
#     path(r'api-token-auth/', vs.obtain_auth_token)
# ]
from rest_framework_jwt.views import obtain_jwt_token
# jwt的认证接口 加$ 符号原因是 防止第三方登陆 login找错路由
urlpatterns += [
    re_path(r'^login/$', obtain_jwt_token),
]

# 第三方登录  url 集成包括login/<backend> complete/<backend>
urlpatterns += [
    path('', include('social_django.urls', namespace='social'))
]

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title="online API",
        default_version='v1',
        description="online生鲜 api",
        terms_of_service="111",
        contact=openapi.Contact(email="11"),
        license=openapi.License(name="11"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# 在原有的路由里面添加一个
urlpatterns += [
	path('api_doc/', schema_view.with_ui('redoc', cache_timeout=0), name="online API"),
    path("pay", AlipayView.as_view(), name="pay"),
    path("alipay/handler", PayHandlerView.as_view(), name="payhandler"),
    path("alipay/return/", AlipayView1.as_view(), name="alipay"),

]

# allauth
urlpatterns += [
    path("accounts/", include("allauth.urls"))
]
