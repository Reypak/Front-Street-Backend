# Databases

## Remote SQL Database

### Install `mysql-connector`

`pip install mysql-connector-python`

### Add configuration

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'your_database_host',  # Set to 'localhost' for local development
        'PORT': '3306',  # Default port for MySQL
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'", "use_pure": True},
    }
}
```

### Run migrations

`python manage.py migrate`

### Setup pooling configuration

```python
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
        'OPTIONS': {
            'autocommit': True,
            'pool_name': 'mypool',
            'pool_size': 5,  # Number of connections to maintain in the pool
            'pool_reset_session': True,  # Reset session state when connection is returned to the pool
            'connection_timeout': 300,  # Timeout for connections in seconds
            'pool_timeout': 30,  # Timeout for getting a connection from the pool
        },
    }
}
```

## Database Connection Pooling (NOT IMPLEMENTED IF USING mysql.connector)

For improved performance, consider using a connection pooler like django-db-connection-pool:

### install dependencies

`pip install django-db-connection-pool`

### Add to apps

```python
INSTALLED_APPS += ['django_db_connection_pool']
```
