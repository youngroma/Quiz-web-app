from decouple import config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='your-secret-key')

DEBUG = config('DEBUG', cast=bool, default=True)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='your_db_name'), # your database name
        'USER': config('DB_USER', default='your_db_user'), # user's name
        'PASSWORD': config('DB_PASSWORD', default='your_password'), # database password
        'HOST': config('DB_HOST', default='localhost'),  # host
        'PORT': config('DB_PORT', default='5432'),  #port
    }
}

# static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'quizes' /  'static'
]

# default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'quizes:main-view'
LOGOUT_REDIRECT_URL = 'login'
