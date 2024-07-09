# Getting Started

<!-- VIRTUAL ENV -->
<details>
<summary>Virtual Environment</summary>

## Create a new virtual environment

`python3 -m venv .venv`

## Activate virtual environment

`. .venv/bin/activate`

</details>

<!-- INSTALLATION -->
<details>
<summary>Installation</summary>

## Install Django

`pip install django`

### Install Django Restframework

To create the REST API

`pip install djangorestframework`

## Create superuser

`python manage.py createsuperuser`

</details>

<!-- PROJECT -->
<details>
<summary>Project</summary>

## Create Django Project

Create Django App inside root directory

`django-admin startproject <app_name> .`

## Create a new app

`python manage.py startapp <app_name>`

</details>

<!-- DATABASE -->
<details>
<summary>Database</summary>

## Flush Database

DESTROY all data currently in the database, and return each table to an empty state.

`python manage.py flush`

</details>

## Start Django Server

`python manage.py runserver`

## Run migrations for app

`python manage.py makemigrations <app_name>`

then run to apply:

`python manage.py migrate`

<!--
<details>
<summary></summary>

</details>
-->

##

# Django REST API

<!-- PACKAGES -->
<details>
<summary>Packages</summary>

## Installed packages

To check installed packages

`pip list`

</details>

<!-- PAGINATION -->
<details>
<summary>Pagination</summary>

## Pagination

Django pagination `rest_framework` must be installed and enabled.

<details>
<summary><b>Default Pagination</b></summary>

## Default Pagination

Add the configuration to the project app `settings.py`

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

</details>

<details>
<summary>Custom Pagination</summary>

## Custom Pagination

For custom pagination you can use the `pagination_class` attribute to add a custom pagination class to the `views.py`(view)

Add to the view:

`pagination_class = CustomPagination`

### The Custom Pagination Class

```python
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 20
```

### Disable pagination

Disable pagination for the viewset

` pagination_class = None`

</details>

</details>

<!-- USERS -->
<details>
<summary>Users</summary>

## Current Default User

`CurrentUserDefault` is a default value class provided by DRF, typically used to set a field's default value to the currently authenticated user.

### Usage

```python
class CreateCurrentUser(serializers.CurrentUserDefault):
```

This defines a new class `CreateCurrentUser` that inherits from `serializers.CurrentUserDefault`.

</details>

<!-- FILTERS -->

## Django Filters

### Install package

`pip install django-filter`

### Installed apps

Add to your `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    'django_filters',
]
```

## Signals

Use Django signals to track create and update

### Register the Signals

Ensure that the signals are registered when the application starts.

```python
# apps.py
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'your_app'

    def ready(self):
        import your_app.signals

```

### Add the AppConfig to Your App

Ensure the custom AppConfig is used in your application settings.

```python
# __init__.py in your_app
default_app_config = 'your_app.apps.YourAppConfig'
```

# Django Model Fields

`blank=True` allows you to input nothing (i.e `""`, `None`) and keep it empty.

`null=True` means the database row is allowed to be `NULL`.

`default=None` sets the field to `None` if no other value is given.

# Saving to Object instance

### Using Model

Overriding the `save` method, and assign a `new value` to the `payment_number` field of the `Payment` object.

```python
# class LoanPayment(BaseModel):
# ....
 def save(self, *args, **kwargs):
        if not self.payment_number:
            self.payment_number = "pass any value"
        super(LoanPayment, self).save(*args, **kwargs)
```

### Using Serializer

Overriding the `create` method, get the field from `validated_data` and update it with a new value

```python
# class LoanPaymentSerializer(BaseSerializer):
# ....
 def create(self, validated_data):
        validated_data['payment_number'] = "pass any value"
        return super().create(validated_data)
```

### Using ViewSet

Overriding the `perform_create` method

```python
# class LoanViewSet(viewsets.ModelViewSet):
def perform_create(self, serializer):
    return serializer.save(created_by=self.request.user)
```

Overriding the `perform_update` method

```python
# class LoanViewSet(viewsets.ModelViewSet):
def perform_update(self, serializer):
    return serializer.save(updated_by=self.request.user)
```

## Overiding Serializer default class

`get_serializer_class`: Returns the class that should be used for the serializer.

### Action Types

'list' , 'create', 'retrieve'

```python
# views.py

# class LoanViewSet(viewsets.ModelViewSet):
# ....
 def get_serializer_class(self):
        if self.action == 'list':
            return LoanListSerializer

        return LoanDetailsSerializer
```

## Get object instance from inside serializer

```python

  def to_representation(self, instance):
        data = super().to_representation(instance)
        # get loan instance
        loan = Loan.objects.get(application=instance.id)
        # serialize loan
        loan_serializer = LoanSerializer(loan)
        # set loan
        data['loan'] = loan_serializer.data
        return data

```

# SQL COMMANDS

## Using db shell (Recommended)

`python manage.py shell`

## Using SQLite Shell

### Open SQLite shell:

Execute the following command to open the SQLite shell and connect to your database file (usually named db.sqlite3):

`sqlite3 db.sqlite3`

Delete user by ID:

```sql
DELETE FROM fs_users_customuser WHERE id = 1;
```

# HELPERS

### Tracing

To handle tracing

```
import pdb
pdb.set_trace()
```

### Inspect DB

To inspect the database structure

`python manage.py inspectdb`

# PRODUCTION

## CORS Headers

Install django CORS Headers and add to installed apps.

`pip install djangorestframework django-cors-headers`

```python
# Include in INSTALLED_APPS:
'corsheaders',

# Include this in MIDDLEWARE:
'corsheaders.middleware.CorsMiddleware',

CORS_ORIGIN_ALLOW_ALL = True
```
