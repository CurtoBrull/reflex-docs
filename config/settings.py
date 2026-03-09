"""
Configuración de Django para el proyecto reflex-docs.
"""

from pathlib import Path
from decouple import config, Csv
import sys
import logging

# Configurar logging con soporte para codificación UTF-8
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Construir rutas dentro del proyecto: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent


# Configuración de desarrollo rápido - no apta para producción
# Ver https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# ADVERTENCIA DE SEGURIDAD: mantener la clave secreta en producción segura
# SECRET_KEY es requerida y debe establecerse en variables de entorno
try:
    SECRET_KEY = config('SECRET_KEY')
    if not SECRET_KEY or len(SECRET_KEY) < 50:
        raise ValueError("SECRET_KEY must be at least 50 characters long")
except Exception as e:
    print(f"ERROR: SECRET_KEY configuration failed: {e}", file=sys.stderr)
    print("Please set SECRET_KEY in your .env file or environment variables.", file=sys.stderr)
    sys.exit(1)

# ADVERTENCIA DE SEGURIDAD: no ejecutar con debug activado en producción
DEBUG = config('DEBUG', default=False, cast=bool)

# Configuración de ALLOWED_HOSTS
# Para desarrollo, por defecto localhost y 127.0.0.1
# Para producción, debe establecerse explícitamente en variables de entorno
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())


# Definición de aplicaciones

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps del proyecto
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Base de datos
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Configuración de base de datos usando PostgreSQL 16 con adaptador psycopg2-binary
# Valida: Requisitos 2.1, 2.2, 2.3, 2.5
# Todas las credenciales se leen desde variables de entorno por seguridad

try:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }
except Exception as e:
    logger.critical(f"ERROR: Database configuration failed: {e}")
    logger.critical("Please set DB_NAME, DB_USER, and DB_PASSWORD in your .env file.")
    logger.critical("See .env.example for reference.")
    sys.exit(1)


# Validación de contraseñas
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internacionalización
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_TZ = True


# Archivos estáticos (CSS, JavaScript, Imágenes)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Tipo de campo de clave primaria por defecto
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Verificación de Conexión a Base de Datos
# Verificar conexión a base de datos en inicio con manejo apropiado de errores
# La aplicación falla rápidamente si la base de datos no está disponible

def verify_database_connection():
    """
    Verificar conexión a base de datos en inicio.
    Falla rápidamente con mensaje de error claro si no se puede establecer la conexión.
    
    Valida: Requisito 2.4 - Sistema SHALL verificar la conexión a la base de datos
    """
    from django.db import connection
    from django.db.utils import OperationalError
    
    try:
        # Intentar establecer conexión a base de datos
        connection.ensure_connection()
        logger.info("Conexión a base de datos verificada exitosamente")
        logger.info(f"  Base de datos: {DATABASES['default']['NAME']}")
        logger.info(f"  Host: {DATABASES['default'].get('HOST', 'N/A')}")
        logger.info(f"  Motor: {DATABASES['default']['ENGINE']}")
    except (OperationalError, UnicodeDecodeError) as e:
        # OperationalError: Problemas de conexión a base de datos
        # UnicodeDecodeError: Problema de codificación psycopg2 en Windows cuando BD no está disponible
        logger.critical("¡Falló la conexión a base de datos!")
        logger.critical(f"  Error: {str(e)[:200]}")  # Limitar longitud del mensaje de error
        logger.critical(f"  Base de datos: {DATABASES['default'].get('NAME', 'N/A')}")
        logger.critical(f"  Host: {DATABASES['default'].get('HOST', 'N/A')}")
        logger.critical(f"  Puerto: {DATABASES['default'].get('PORT', 'N/A')}")
        logger.critical("")
        logger.critical("Por favor verificar:")
        logger.critical("  1. El servidor PostgreSQL está ejecutándose")
        logger.critical("  2. Las credenciales de base de datos en .env son correctas")
        logger.critical("  3. La base de datos existe y el usuario tiene acceso")
        logger.critical("  4. Conectividad de red al host de base de datos")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Error inesperado durante conexión a base de datos: {type(e).__name__}")
        logger.critical(f"  Error: {str(e)[:200]}")
        sys.exit(1)

# Solo verificar conexión cuando se ejecuta el servidor o migraciones
# Omitir para otros comandos de gestión para evitar verificaciones innecesarias
if 'runserver' in sys.argv or 'migrate' in sys.argv or 'gunicorn' in sys.argv[0]:
    verify_database_connection()
