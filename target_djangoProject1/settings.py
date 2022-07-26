"""
Django settings for target_djangoProject1 project.

Generated by 'django-login startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import datetime
import os
from pathlib import Path
from login.auth_password_validators import ComplexityValidator

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&z#rogy7*c7k)xx8*9-p4f!idi3ry#4ist8mddchr8&63uv_bx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '0.0.0.0:8000', '127.0.0.1', '8.142.91.1']
# ALLOWED_HOSTS = ['localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',  # 登录与用户
    'propertyManage',  # 资产管理
    'riskWarning',  # 风险管理
    'authorizationManage',  # 授权管理
    'loginLocationManage',  # 登录管理

    'django_apscheduler',  # 定时任务
    'captcha',  # 图形验证码
    'django_user_agents',  # 分析用户UA
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 自定义中间件
    'target_djangoProject1.LogMiddleware.RequestLogMiddleware',  # 记录日志
    'django_user_agents.middleware.UserAgentMiddleware',    # 分析UA的
]

ROOT_URLCONF = 'target_djangoProject1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'target_djangoProject1.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'NAME': 'target_db',  # 数据库名称
        'HOST': '127.0.0.1',  # 数据库地址，本机 ip 地址 127.0.0.1
        'PORT': 3306,  # 端口
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '123456',  # 数据库密码
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
    {
        'NAME': 'login.auth_password_validators.ComplexityValidator'
    },
]

PASSWORD_COMPLEXITY = {  # You can omit any or all of these for no limit for that particular set
    "UPPER": 1,  # Uppercase
    "LOWER": 1,  # Lowercase
    "LETTERS": 1,  # Either uppercase or lowercase letters
    "DIGITS": 1,  # Digits
    "SPECIAL": 1,  # Not alphanumeric, space or punctuation character
    "WORDS": 1  # Words (alphanumeric sequences separated by a whitespace or punctuation character)
}
# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# STATIC_ROOT = '/home/static/'
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 发送邮件配置
EMAIL_USE_SSL = True

EMAIL_HOST = 'smtp.qq.com'  # 如果是 163 改成 smtp.163.com
EMAIL_PORT = 465
EMAIL_HOST_USER = '2372977246@qq.com'  # 账号
EMAIL_HOST_PASSWORD = 'wtaybvwadmiudhfj'  # 授权码
# 默认邮件
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# 缓存
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

"""
    TimedRotatingFileHandler 会按照时间自动切分日志，但是在指定时间没有切分日志后，
    下次运行将会报错。由于要同时切分日志和记录日志，显示文件被占用。

    解决方法：将日志记录目录“web-log.log”的内容清空即可。
"""
# 日志记录
LOGS_DIR = './logs/accessLogs'
LOGGING = {
    # 版本
    'version': 1,
    # 是否禁止默认配置的记录器
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '{"time": "%(asctime)s", "level": "%(levelname)s", "method": "%(method)s", "username": "%('
                      'username)s", "sip": "%(sip)s", "dip": "%(dip)s", "path": "%(path)s", "status_code": "%('
                      'status_code)s", "reason_phrase": "%(reason_phrase)s", "func": "%(module)s.%(funcName)s:%('
                      'lineno)d",  "message": "%(message)s", "http_user_agent": "%(http_user_agent)s", "server_name": '
                      '"%(server_name)s", "body": "%(body)s"}',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        }
    },
    # 定义过滤器
    'filters': {
        'request_info': {'()': 'target_djangoProject1.LogMiddleware.RequestLogFilter'},
    },
    # 定义处理程序
    'handlers': {
        # 标准输出
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # 自定义 handlers，输出到文件
        'restful_api': {
            'level': 'DEBUG',
            # 时间滚动切分
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'web-log.log'),
            'formatter': 'standard',
            # 调用过滤器
            'filters': ['request_info'],
            # 每天凌晨切分
            'when': 'MIDNIGHT',
            # 保存 30 天
            'backupCount': 30,
        },
    },
    # 记录器
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False
        },
        'web.log': {
            'handlers': ['restful_api'],
            'level': 'INFO',
            # 此记录器处理过的消息就不再让 django 记录器再次处理了
            'propagate': False
        },
    }
}

# session配置
SESSION_COOKIE_AGE = 60 * 60 * 24 * 3  # 3天过期

"""
 apscheduler
 用于定时任务的py库，需要定义django-admin命令
 见riskWarning/management/commands/disposeAccessLogs.py
 必须新建management/commands/目录
"""
# Django调度器后台管理界面中显示的时间格式
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
# Seconds，超时时间25s
APSCHEDULER_RUN_NOW_TIMEOUT = 25

# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = 'default'
