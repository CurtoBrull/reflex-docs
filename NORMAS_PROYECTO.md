# Normas del Proyecto Reflex Documentation

## Idioma del Código

### Regla General
**TODOS los comentarios, docstrings y mensajes en el código DEBEN estar en ESPAÑOL.**

### Aplicación
- ✅ Comentarios en Python: español
- ✅ Docstrings de funciones y clases: español
- ✅ Mensajes de log: español
- ✅ Mensajes de error: español
- ✅ Comentarios en Dockerfile: español
- ✅ Comentarios en archivos de configuración: español
- ✅ Documentación inline: español

### Excepciones
- ❌ Nombres de variables, funciones y clases: inglés (convención de Django/Python)
- ❌ Nombres de archivos: inglés (convención de Django)
- ❌ URLs y rutas: inglés
- ❌ Nombres de campos de base de datos: inglés

### Ejemplos

#### ✅ Correcto
```python
def verify_database_connection():
    """
    Verificar conexión a base de datos en inicio.
    Falla rápidamente con mensaje de error claro si no se puede establecer la conexión.
    """
    try:
        # Intentar establecer conexión a base de datos
        connection.ensure_connection()
        logger.info("Conexión a base de datos verificada exitosamente")
    except OperationalError as e:
        # Problemas de conexión a base de datos
        logger.critical("¡Falló la conexión a base de datos!")
```

#### ❌ Incorrecto
```python
def verify_database_connection():
    """
    Verify database connection on startup.
    Fails fast with clear error message if connection cannot be established.
    """
    try:
        # Attempt to establish database connection
        connection.ensure_connection()
        logger.info("Database connection verified successfully")
    except OperationalError as e:
        # Database connection issues
        logger.critical("Database connection failed!")
```

## Estructura del Proyecto

### Organización de Archivos
```
reflex-docs/
├── config/              # Configuración principal de Django
│   ├── settings.py      # Configuración del proyecto
│   ├── urls.py          # URLs principales
│   └── wsgi.py          # Configuración WSGI
├── core/                # App principal
├── tutorials/           # App de tutoriales
├── components/          # App de componentes
├── playground/          # App de ejemplos de código
├── accounts/            # App de gestión de usuarios
├── static/              # Archivos estáticos
├── templates/           # Plantillas HTML
├── manage.py            # Utilidad de línea de comandos
├── requirements.txt     # Dependencias de producción
├── requirements-dev.txt # Dependencias de desarrollo
├── Dockerfile           # Configuración de Docker
├── .dockerignore        # Exclusiones de Docker
├── .env                 # Variables de entorno (no versionar)
├── .env.example         # Ejemplo de variables de entorno
└── .gitignore           # Exclusiones de Git
```

## Configuración Regional

### Idioma y Zona Horaria
```python
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_TZ = True
```

## Gestión de Variables de Entorno

### Variables Requeridas
- `SECRET_KEY`: Clave secreta de Django (mínimo 50 caracteres)
- `DEBUG`: Modo debug (True/False)
- `ALLOWED_HOSTS`: Hosts permitidos (separados por comas)
- `DB_NAME`: Nombre de la base de datos
- `DB_USER`: Usuario de la base de datos
- `DB_PASSWORD`: Contraseña de la base de datos
- `DB_HOST`: Host de la base de datos (default: localhost)
- `DB_PORT`: Puerto de la base de datos (default: 5432)

### Seguridad
- ❌ NUNCA versionar el archivo `.env`
- ✅ Siempre usar `.env.example` como referencia
- ✅ Validar variables requeridas en `settings.py`
- ✅ Fallar rápidamente con mensajes claros si faltan variables

## Base de Datos

### PostgreSQL
- Versión: PostgreSQL 16
- Adaptador: psycopg2-binary
- Verificación de conexión en inicio
- Manejo de errores con mensajes claros en español

## Docker

### Imagen Base
- `python:3.12-slim`

### Variables de Entorno
- `PYTHONDONTWRITEBYTECODE=1`: Prevenir archivos .pyc
- `PYTHONUNBUFFERED=1`: Logs inmediatos

### Dependencias del Sistema
- `libpq-dev`: Biblioteca cliente de PostgreSQL
- `gcc`: Compilador C para paquetes de Python

## Estilo de Código

### Python
- Seguir PEP 8
- Usar flake8 para linting (max-line-length: 120)
- Comentarios y docstrings en español
- Nombres de variables/funciones en inglés

### Django
- Seguir convenciones de Django
- Apps modulares con responsabilidades claras
- Modelos con docstrings en español
- Vistas basadas en clases cuando sea apropiado

## Testing

### Estrategia Dual
1. **Unit Tests**: Casos específicos y edge cases
2. **Property-Based Tests**: Propiedades universales con Hypothesis

### Cobertura
- Objetivo mínimo: 80%
- 100% en rutas críticas (autenticación, persistencia)

### Frameworks
- Django's built-in test framework
- pytest-django
- Hypothesis (property-based testing)

## Git

### Estrategia de Ramas
- `main`: Código de producción
- `develop`: Integración
- `feature/*`: Nuevas funcionalidades
- `hotfix/*`: Correcciones urgentes

### Commits
- Mensajes descriptivos en español
- Commits atómicos
- Referenciar issues cuando aplique

## CI/CD

### Pipeline CI
- Trigger: Pull requests a main/develop
- Ejecutar: flake8, tests
- Bloquear merge si falla

### Pipeline CD
- Trigger: Push a main
- Desplegar automáticamente
- Ejecutar migraciones

## Documentación

### Código
- Docstrings en español para todas las funciones públicas
- Comentarios inline en español para lógica compleja
- Referencias a requisitos cuando aplique

### Proyecto
- README.md con instrucciones de instalación
- .env.example con todas las variables documentadas
- Documentación de API cuando aplique

## Logging

### Niveles
- `INFO`: Información general (conexiones exitosas, inicio de servicios)
- `WARNING`: Advertencias (configuraciones subóptimas)
- `ERROR`: Errores recuperables
- `CRITICAL`: Errores fatales (fallo de conexión a BD)

### Formato
- Mensajes en español
- Incluir contexto relevante
- Usar logger en lugar de print()

## Seguridad

### Buenas Prácticas
- SECRET_KEY en variables de entorno
- DEBUG=False en producción
- ALLOWED_HOSTS configurado apropiadamente
- Validación de entrada de usuario
- Protección CSRF habilitada
- Contraseñas hasheadas (Django por defecto)

## Mantenimiento

### Dependencias
- Mantener requirements.txt actualizado
- Separar dependencias de desarrollo
- Documentar versiones específicas cuando sea necesario

### Migraciones
- Crear migraciones para todos los cambios de modelo
- Revisar migraciones antes de aplicar
- Nunca editar migraciones aplicadas

---

**Última actualización**: 2024
**Versión**: 1.0
