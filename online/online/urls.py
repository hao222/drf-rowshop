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

import xadmin
from online.settings import MEDIA_ROOT
from django.views.static import serve

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as vs
# from goods.views_base import GoodsListView
from goods.views import GoodsListViewSet, CategoryViewSet
from goods import views

router = DefaultRouter()
#配置goods的url
router.register(r'goods', GoodsListViewSet, base_name="goods")

#配置goodscategory的url
router.register(r'goods', CategoryViewSet, base_name="categorys")

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('docs/', include_docs_urls(title="online商品"))
]

# drf 自带的认证模式该路由返回一个json格式的{ 'token' : '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'}  保存到我们的数据库的那个token表
# urlpatterns += [
#     path(r'api-token-auth/', vs.obtain_auth_token)
# ]
from rest_framework_jwt.views import obtain_jwt_token
# jwt的认证接口
urlpatterns += [
    path(r'login/', obtain_jwt_token),
]
