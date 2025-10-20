"""
Django settings for marketplace_lust project.
"""

from pathlib import Path
from decouple import config
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = config('SECRET_KEY', default='django-insecure-9o@7sujjvz)8b^7$7&o)x$lh*9h#5p0dq+2st2v+ybjq$gf_$a')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    # Local apps
    'productos',
    'VirtualR',
    'Carrito',
    'payments',
    'authentication', 
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'marketplace_lust.urls'

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
                'marketplace_lust.context_processors.carrito_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'marketplace_lust.wsgi.application'

# ✅ DATABASE - POSTGRESQL (CONFIGURADO)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='lustplace_db'),
        'USER': config('DB_USER', default='admin'),
        'PASSWORD': config('DB_PASSWORD', default='admin123'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# ✅ FALLBACK A SQLITE PARA DESARROLLO (COMENTADO)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# REST FRAMEWORK + JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# ✅ AGREGAR JWT SETTINGS
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# ✅ AGREGAR CORS SETTINGS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
CORS_ALLOW_CREDENTIALS = True

# ✅ INTERNACIONALIZACIÓN - DEFAULT (flexible)
LANGUAGE_CODE = 'en-us'  # ← Mantener default
TIME_ZONE = 'UTC'        # ← Mantener default
USE_I18N = True
USE_TZ = True

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

# ✅ CONFIGURACIÓN DE MEDIOS
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ✅ CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ✅ CONFIGURACIÓN DE IMÁGENES
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# ✅ FORMATOS PERMITIDOS
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# Login settings
LOGIN_REDIRECT_URL = 'lista_productos'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'lista_productos'

# ✅ CONFIGURACIÓN DE GOOGLE OAUTH
GOOGLE_OAUTH2_CLIENT_ID = config('GOOGLE_CLIENT_ID', default='758944758855-0ej7l6t3rijbefthjdp2e75bmdvup6hr.apps.googleusercontent.com')
GOOGLE_OAUTH2_CLIENT_SECRET = config('GOOGLE_CLIENT_SECRET', default='')

# URLs de callback para Google OAuth
GOOGLE_OAUTH_CALLBACK_URL = 'http://127.0.0.1:8000/auth/google/'
GOOGLE_OAUTH_SUCCESS_REDIRECT = 'perfil_usuario'
GOOGLE_OAUTH_ERROR_REDIRECT = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
