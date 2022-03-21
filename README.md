# Deadline as a Service

We are making a vending machine with micro:bit and a lot of shit this time

## Getting started

You don't

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
