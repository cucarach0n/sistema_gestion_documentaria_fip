from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = config('IP_SERVER').split(',')


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DATA_BASE'),
        'USER': config('DATA_BASE_USER'),
        'PASSWORD': config('DATA_BASE_PASSWORD'),
        'HOST': config('DATA_BASE_HOST'),
        'PORT': '',
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'portalmy_uni',
        'USER': 'portalmy_uniuser',
        'PASSWORD':'unisistema2022',
        'HOST': 'portalmybot.com',
        'PORT': '',
    }
}
'''
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

EMAIL_HOST = 'mail.fipdigital.info'
EMAIL_PORT = 26
EMAIL_HOST_USER = config('USER_MAIL_ADDRESS')
EMAIL_HOST_PASSWORD = config('USER_MAIL_PASSWORD')
EMAIL_USE_TLS = False

print("Local ON")