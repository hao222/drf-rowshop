"""
Django settings for online project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
import datetime
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# apps和extra_apps mark source root 这样可以直接通过app import
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5hvq6jgif&7bj6=6ma4m6(ifbn#kw%0el+&n$zd%d%hqwdx3%b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'users.UserApp'


# django 默认的auth认证 是比对用户名和密码   为此我们可以设置一个函数 来自定义django认证
AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
    'social_core.backends.weibo.WeiboOAuth2',
    'social_core.backends.qq.BaseOAuth2',
    'social_core.backends.weixin.WeixinOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'DjangoUeditor',
    'goods.apps.GoodsConfig',
    'trade',
    'user_operation',
    'crispy_forms',
    'xadmin',
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',   # 使用 TokenAuthentication 时候 需要用到，会生成token表，此处弃用
    'corsheaders',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 允许所有
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'online.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'online.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "vueshop",
        'USER': "root",
        'PASSWORD': "123456",
        'HOST': '127.0.0.1',
        # 'OPTIONS':{'init_command':'SET storage_engine=INNODB;'}
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # 当地时间


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE':9,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',       # 会要求浏览器提供 用户名  密码
        'rest_framework.authentication.SessionAuthentication',  # 这俩个是默认配置 以便登录接口文档 实际用的是django的中间件  是为验证用户信息
        # 'rest_framework.authentication.TokenAuthentication',    # 这个为 token 认证方式 每个接口调用时 都会经过验证 user 为request 返回user  用于登录
        # JWT 是我们这次要使用的验证方式，但不是全局验证  因为如果在访问页面时，token过期了，那么就会导致错误。
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    # ddrf 设置api的访问速率  通常是为了防止 在一段时间内 爬虫的操作
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',    # 用户登录之前， 通过ip地址判断
        'rest_framework.throttling.UserRateThrottle'     # 用户登录后  通过token判断
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '2/minute',
        'user': '3/minute'
    }
}

# JWT设置
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7), #7天过期时间
    'JWT_AUTH_HEADER_PREFIX': 'JWT', # 默认设置认证
}

# 手机正则
REGEX_PHONE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

# 云片网设置
APIKEY = "4f50ae2bdef057fe764d58fd1c484bdf"

# 公共的数据可以添加缓存
#   drf cache 缓存过期时间
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 15        # 过期时间15秒
}

# redis 作为缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": "redis://:123456@127.0.0.1:6379",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# 微博开发平台  app_key   secret
SOCIAL_AUTH_WEIBO_KEY = '3604588907'
SOCIAL_AUTH_WEIBO_SECRET = 'd4b6f86e71a9a960e48513e11a0c2352'

SOCIAL_AUTH_QQ_KEY = 'foobar'
SOCIAL_AUTH_QQ_SECRET = 'bazqux'

SOCIAL_AUTH_WEIXIN_KEY = 'foobar'
SOCIAL_AUTH_WEIXIN_SECRET = 'bazqux'

# 登录成功之后 王什么地方跳转
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/index/'
