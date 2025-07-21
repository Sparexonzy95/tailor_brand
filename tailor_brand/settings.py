import os
from pathlib import Path
from decouple import config
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# === SECURITY SETTINGS ===
SECRET_KEY = config('SECRET_KEY', default='your-fallback-secret-key-for-local-dev-only')
DEBUG = config('DEBUG', default=True, cast=bool)
ENVIRONMENT = config('ENVIRONMENT', default='development')

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # Add for WhiteNoise to handle static files in development
    'django.contrib.staticfiles',
    'cloudinary_storage',  # Must come before staticfiles
    'cloudinary',
    'website',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add WhiteNoise middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tailor_brand.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tailor_brand.wsgi.application'

# === DATABASE CONFIGURATION ===
if ENVIRONMENT == 'production' and 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ['DATABASE_URL'],
            conn_max_age=600,
            conn_health_checks=True,  # Enable health checks for better connection handling
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# === STATIC FILES ===
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'website/static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# === MEDIA FILES ===
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# === CLOUDINARY CONFIG ===
cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME', default=''),
    api_key=config('CLOUDINARY_API_KEY', default=''),
    api_secret=config('CLOUDINARY_API_SECRET', default=''),
    secure=True
)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default=''),
    'API_KEY': config('CLOUDINARY_API_KEY', default=''),
    'API_SECRET': config('CLOUDINARY_API_SECRET', default=''),
    'SECURE': True,
    'MEDIA_TAG': 'media',
    'INVALID_VIDEO_ERROR_MESSAGE': 'Please upload a valid video file.',
    'EXCLUDE_DELETE_ORPHANED_MEDIA_PATHS': (),
    'MAGIC_FILE_PATH': 'Uploads/',
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# === EMAIL CONFIGURATION ===
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=465, cast=int)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='Bibiartisan <logicbloomlab@gmail.com>')

# === LOGGING CONFIGURATION ===
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/debug.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
        },
    },
}

# === SECURITY SETTINGS FOR PRODUCTION ===
if ENVIRONMENT == 'production':
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    CSRF_TRUSTED_ORIGINS = config(
        'CSRF_TRUSTED_ORIGINS',
        default='https://*.onrender.com',
        cast=lambda v: [s.strip() for s in v.split(',')]
    )
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'