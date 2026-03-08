# reflex-docs

Sistema web de documentación y aprendizaje para el framework [Reflex](https://reflex.dev) (Python full-stack framework). Construido con Django, PostgreSQL y Docker.

## Características

- **Tutoriales**: Contenido educativo paso a paso
- **Referencia de componentes**: Documentación de la API de Reflex
- **Playground**: Ejemplos de código con resaltado de sintaxis (highlight.js)
- **Cuentas de usuario**: Registro, autenticación y perfiles
- **Panel de administración**: Gestión de contenido via Django Admin
- **CI/CD**: Pipelines automáticos con GitHub Actions

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | Django + Python 3.12 |
| Base de datos | PostgreSQL 16 |
| Servidor WSGI | Gunicorn |
| Reverse proxy | Nginx |
| Estilos | TailwindCSS (CDN) |
| Resaltado de código | highlight.js (CDN) |
| Contenedores | Docker + Docker Compose |

## Requisitos previos

- [Docker](https://docs.docker.com/get-docker/) >= 24
- [Docker Compose](https://docs.docker.com/compose/install/) >= 2

## Inicio rápido (desarrollo local)

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd reflex-docs
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus valores
```

### 3. Levantar los servicios

```bash
docker compose up --build
```

La aplicación estará disponible en [http://localhost:8000](http://localhost:8000).

### 4. Ejecutar migraciones (primera vez)

```bash
docker compose exec web python manage.py migrate
```

### 5. Crear superusuario

```bash
docker compose exec web python manage.py createsuperuser
```

El panel de administración estará en [http://localhost:8000/admin](http://localhost:8000/admin).

## Variables de entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta de Django | `django-insecure-...` |
| `DEBUG` | Modo debug | `True` / `False` |
| `ALLOWED_HOSTS` | Hosts permitidos | `localhost,127.0.0.1` |
| `DB_NAME` | Nombre de la base de datos | `reflex_docs` |
| `DB_USER` | Usuario de PostgreSQL | `postgres` |
| `DB_PASSWORD` | Contraseña de PostgreSQL | `password` |
| `DB_HOST` | Host de PostgreSQL | `db` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |

## Estructura del proyecto

```
reflex-docs/
├── config/                 # Configuración principal de Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                   # App: páginas principales y navegación
├── tutorials/              # App: tutoriales paso a paso
├── components/             # App: referencia de componentes Reflex
├── playground/             # App: ejemplos de código interactivos
├── accounts/               # App: registro, autenticación y perfiles
├── static/                 # Archivos estáticos
├── templates/              # Plantillas HTML globales
├── tests/                  # Tests del proyecto
│   ├── unit/
│   ├── property/
│   └── integration/
├── docker-compose.yml      # Entorno de desarrollo
├── docker-compose.prod.yml # Entorno de producción
├── Dockerfile
├── nginx.conf
├── requirements.txt
├── requirements-dev.txt
└── manage.py
```

## Ejecutar tests

```bash
# Todos los tests
docker compose exec web python manage.py test

# Con coverage
docker compose exec web coverage run -m pytest
docker compose exec web coverage report

# Solo property tests
docker compose exec web pytest tests/property/

# Linting
docker compose exec web flake8 . --max-line-length=120 --exclude=migrations
```

## Despliegue en producción

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

El servicio de producción ejecuta automáticamente migraciones y `collectstatic` al arrancar.

### Secrets requeridos para CI/CD

Configura los siguientes secrets en GitHub Actions (`Settings > Secrets`):

| Secret | Descripción |
|--------|-------------|
| `SERVER_HOST` | IP o dominio del servidor |
| `SERVER_USER` | Usuario SSH |
| `SERVER_SSH_KEY` | Clave privada SSH |

## Estrategia de ramas

| Rama | Propósito |
|------|-----------|
| `main` | Código de producción |
| `develop` | Integración de features |
| `feature/*` | Nuevas funcionalidades |
| `hotfix/*` | Correcciones urgentes |

Los PRs hacia `main` y `develop` requieren que el pipeline de CI pase (linting + tests).

## URLs principales

| URL | Descripción |
|-----|-------------|
| `/` | Página de inicio |
| `/tutorials/` | Lista de tutoriales |
| `/components/` | Referencia de componentes |
| `/playground/` | Ejemplos de código |
| `/accounts/register/` | Registro de usuario |
| `/accounts/login/` | Login |
| `/admin/` | Panel de administración |

## Licencia

MIT
