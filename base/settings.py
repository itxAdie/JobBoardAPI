import datetime
import os
from pathlib import Path

from decouple import config

from base.log_filters import ExcludeStatReloaderFilter, TraceIDFilter

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Path to log directory
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# Create log directory if it doesn't exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

DEVELOPMENT = config('ENV') == 'development'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if DEVELOPMENT else False

CORS_ORIGIN_ALLOW_ALL = True

MAX_UPLOAD_SIZE = 5242880  # 5MB

ALLOWED_HOSTS = [
    '*', 'localhost',
]

CSRF_TRUSTED_ORIGINS = [
]

# Application definition
INSTALLED_APPS = [
    'common.apps.CommonConfig',
    'auth_control.apps.AuthControlConfig',
    'user_control.apps.UserControlConfig',
    'resume_control.apps.ResumeControlConfig',
    'job_control.apps.JobControlConfig',
    'test_control.apps.TestControlConfig',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    "django_filters",
    "jazzmin",
    'corsheaders',
    'import_export',
    'rest_framework_swagger',  # Swagger
    'drf_yasg',  # Yet Another Swagger generator

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'base.middleware.RequestLogMiddleware',
    'base.middleware.TraceIDMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
]

AUTH_USER_MODEL = "user_control.UserModel"

ROOT_URLCONF = 'base.urls'

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

WSGI_APPLICATION = 'base.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'exclude_state_reloader': {
            '()': ExcludeStatReloaderFilter,
        },
        'trace_id_filter': {
            '()': TraceIDFilter,
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {trace_id} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {trace_id} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'filters': ['exclude_state_reloader', 'trace_id_filter'],
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'formatter': 'verbose',
            'when': 'midnight',  # Rotate logs at midnight
            'interval': 1,  # Rotate daily
            'backupCount': 30,  # Keep logs for 30 days
        },
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['trace_id_filter'],
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "Asia/Dhaka"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STORAGE_TYPE = config('STORAGE_TYPE', default='local')
SERVER_URL = config('SERVER_URL', default='http://127.0.0.1:8000')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configure Django Jazzmin
JAZZMIN_SETTINGS = {
    'site_title': 'Job Board',
    'site_header': 'Job Board',
    # 'site_logo': 'https://www.tiger11.pro/static/media/logo.8af75a0c29cf776d4b1f.png',
    'welcome_sign': 'Welcome to Job Board',
    # 'search_model': 'auth.User',
    'user_avatar': None,
    # 'topmenu_links': [
    #     {'name': 'Home', 'url': 'admin:index', 'permissions': ['auth.view_user']},
    #     {'name': 'Settings', 'url': 'admin:app_list', 'permissions': ['auth.view_user']},
    # ],
    'show_ui_builder': True,
    'navigation_expanded': True,
    'hide_apps': [],
    'hide_models': [],
    'related_modal_active': False,
    'custom_css': None,
    'custom_js': None,
    'show_drug_title': True,
    'drug_title': 'Tiger11',
    'site_url': 'https://api.tiger11.pro/',
    'show_full_screen': True,
    # 'changeform_format': 'horizontal_tabs',
    # 'changeform_format_overrides': {
    #     'auth.user': 'vertical_tabs',
    # },
    'theme': 'default',
    'icon_theme': 'default',
    # 'favicon': 'https://www.tiger11.pro/static/media/logo.8af75a0c29cf776d4b1f.png',
    'default_icon_parents': 'fas fa-fw fa-folder',
    'default_icon_children': 'fas fa-fw fa-file',
}

# Configure Django CORS Headers
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:8000',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8000',
]

# Configure Django Import Export
IMPORT_EXPORT_USE_TRANSACTIONS = True
IMPORT_EXPORT_SKIP_ADMIN_LOG = True
IMPORT_EXPORT_IMPORT_PERMISSION_CODE = 'import_export.import_data'
IMPORT_EXPORT_EXPORT_PERMISSION_CODE = 'import_export.export_data'
IMPORT_EXPORT_RESOURCE_CLASS = 'import_export.resources.ModelResource'

# Configure Django Rest Framework
REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY': 'error',
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DATETIME_INPUT_FORMATS': ['%Y-%m-%d %H:%M', '%Y-%m-%d'],
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M',  # For Am/Pm: %Y-%m-%d %I:%M %p
}

# Configure Django Rest Framework Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(hours=12),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# Configure Django Rest Framework Swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

# Configure the Debug Toolbar
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
    ]
    INTERNAL_IPS = [
        # Add your IP address(es) for accessing the toolbar
        '127.0.0.1',
    ]
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    }

# Configure the WhiteNoise
WHITENOISE_AUTOREFRESH = True
