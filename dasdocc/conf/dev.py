import os
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Moritz Krog', 'moritzkrog@gmail.com'),
)

MANAGERS = ADMINS

MEDIA_ROOT = os.path.join(BASE_DIR, '/media/')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, '/static/')

STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'