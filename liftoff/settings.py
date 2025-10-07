from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl
import logging



logging.basicConfig(level=logging.DEBUG)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3j)hc*!s-$lth0n9o*th#$-sw(t*w@=j$q$9f80zffil*g5+a_'

#DATABASE_URL = 'postgresql://liftoff_jelibit_user:51nhYy1v7aope9NyVmEbrMWozoIViJse@dpg-d2sv15nfte5s739n2jl0-a/liftoff_jelibit'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '10.0.2.2','liftoff-mmaa.onrender.com',]


CORS_ALLOWED_ORIGINS = ['http://localhost:3000',
                        'http://10.0.2.2:8000',
                        'http://192.168.0.1:8000',
                        'https://liftoff-mmaa.onrender.com',
                        'http://127.0.0.1:5500',
                        ] 
#not in productions
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
# Application definition

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'cache-control',
]



from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}




INSTALLED_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth',
    'dj_rest_auth.registration',  # For registration endpoints
    'jelibit',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Sites framework (set site_id=1 in your DB or admin)
SITE_ID = 1

AUTHTENTICATION_BACKEND = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]



MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serves static files
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'liftoff.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'liftoff.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases



  

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


AUTH_USER_MODEL = 'jelibit.CustomUser'



DATABASES = {
    'default': dj_database_url.config(
        default="postgresql://jelibit_databasetwo_user:WjJEDL8HRz6tLpz2ILHNwQejvIBs7B7a@dpg-d3ie2oogjchc73e9v97g-a/jelibit_databasetwo",
#        default=os.environ.get('DATABASE_URL', 'postgresql://jelibit_database_user:    KfqTKHPLVnCGb1yfOwA3023GODRIe0Us@dpg-d2tb99vdiees7383lls0-a/jelibit_database'), --- IGNORE ---  
        conn_max_age=600,
        ssl_require=True
    )
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Where collectstatic will output files
# Use WhiteNoise for serving static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}
REST_AUTH = {
    'REGISTER_SERIALIZER': 'jelibit.serializers.RegisterSerializer',
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'jwt-auth',
    'JWT_AUTH_REFRESH_COOKIE': 'jwt-refresh',
}





EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "belloabdulrahmon345@gmail.com"
EMAIL_HOST_PASSWORD = "kaqs advy leih mkwe"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER





SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'app' :{
            'Client_id': '76404664548-c4jme9v410f5i6nhl1svrj3q4a6qr90q.apps.googleusercontent.com',
            'secret' : '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',
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}


SOCIALACCOUNT_LOGIN_ON_GET =True
LOGIN_REDIRECT_URL ='broadcast'


# Configure django-allauth to use the correct username field
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'  # Replace 'email' with the field you use as USERNAME_FIELD
ACCOUNT_USERNAME_REQUIRED = False  # If you’re not using a username field
ACCOUNT_EMAIL_REQUIRED = True  # If email is the primary identifier
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Use email for authentication
