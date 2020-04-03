## Project setup.

1. Create a .env file under src folder with the following setting. 

```shell script
DJANGO_SETTINGS_MODULE="sentinel.settings_local"
```

2. Create settings_local.py file under src/sentinel

```python
from  .settings_base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'Database name',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'db_username',
        'PASSWORD': 'db_password',
        'HOST': 'db_host',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '5432',                      # Set to empty string for default.
    }
}

DEBUG = True
```

3. Install packages 

```shell script
#cd src
#pip3 install -r requirements.txt 
```

4. Migrate & runserver

```shell script
#cd src
#python3 manage.py migrate
#python3 manage.py runserver 
```