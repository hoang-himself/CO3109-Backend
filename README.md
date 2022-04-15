# Deadline as a Service

[![CI](https://github.com/Smithienious/CO3109-Backend/actions/workflows/main.yml/badge.svg)](https://github.com/Smithienious/CO3109-Backend/actions/workflows/main.yml)

We are making a vending machine with micro:bit and a lot of shit this time

## Getting started

0. Prerequisites
   - [Docker](https://www.docker.com/)
   - [VSCode](https://code.visualstudio.com/)
   - [Remote Development](https://aka.ms/vscode-remote/download/extension)
1. Open VSCode in this folder
2. Create a file named `.env` at the root of this folder according to this format

   ```bash
   # from django.core.management.utils import get_random_secret_key
   # get_random_secret_key()
   SECRET_KEY='<fill your seed here>'
   JWT_KEY='<fill your seed here>'

   # Postgres
   # If you change any of these POSTGRES parameters, you have to update DATABASE_URL too
   POSTGRES_USER=what-is-love
   POSTGRES_PASSWORD=baby-dont-hurt-me
   POSTGRES_DB=no-more
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432

   # Django
   HOST=0.0.0.0
   PORT=3109
   # postgres://<DB user>:<DB user password>@<host>:<port>/<DB name>
   DATABASE_URL=postgres://what-is-love:baby-dont-hurt-me@postgres:5432/no-more

   ```

3. `Command Palette` -> `Remote-Containers: Reopen in Container`

## Utility functions

### Clear cache and migrations file

```bash
find . -type f -name "*.py[co]" -delete
find . -type d -name "__pycache__" -delete
find . -depth -type d -name ".mypy_cache" -exec rm -r {} +
find . -depth -type d -name ".pytest_cache" -exec rm -r {} +
find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "*/db/*" -delete

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
```

### Generate SECRET_KEY and JWT_KEY

```python
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```
