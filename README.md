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

<!-- MIGRATIONS -->
<details>
<summary>Migrations</summary>

## Run migrations for app

`python manage.py makemigrations <app_name>`

then run to apply:

`python manage.py migrate`

</details>

<details>
<summary>Run Server</summary>

## Start Django Server

`python manage.py runserver`

</details>

<!-- <details>
<summary></summary>

</details> -->

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

```ruby
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

```ruby
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 20
```

</details>

</details>

<!-- USERS -->
<details>
<summary>Users</summary>

## Current Default User

`CurrentUserDefault` is a default value class provided by DRF, typically used to set a field's default value to the currently authenticated user.

### Usage

```ruby
class CreateCurrentUser(serializers.CurrentUserDefault):
```

This defines a new class `CreateCurrentUser` that inherits from `serializers.CurrentUserDefault`.

</details>
