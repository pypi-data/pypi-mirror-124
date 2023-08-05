# django-audit


![GitHub issues](https://img.shields.io/github/issues/Emmarex/django-audit)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django_audit)

Django Audit is a simple Django app that tracks and logs requests to your application.

## Quick Start
1. Install django-audit

```bash 
pip install django-audit
```

2. Add ```django_audit``` to your INSTALLED_APPS:

```python
INSTALLED_APPS = [
    ...,
    "django_audit"
]
```

3. Add ```django_audit``` middleware:

```python
MIDDLEWARE = [
    ...
    "django_audit.middleware.AuditMiddleware"
]
```

4. Run migrate

```bash
python manage.py migrate
```