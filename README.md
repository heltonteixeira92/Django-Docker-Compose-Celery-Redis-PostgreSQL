# Django-Docker-Compose-Celery-Redis-PostgreSQL

Process of setting up a Docker Compose file to create a Django, Redis, Celery and PostgreSQL environment.
That allow you to work with the named tools without having to installing them in your OS environment.

`Celery` unlocks worker process for django

`Redis` is the datastore and message broker between Celery and Django.

- Django and Celery use Redis to communite with each other (instead of SQL DB)
- Redis Can also be used as a cache as well.
- An `alternative` for Django & Celery is `RabbitMQ`

All three work together to make some `asynchronous` magic.


### Here's a few great use cases for Django + Celery:
- Seding emails and/or email notifications
- Run specific functions on a schedulo
- Backup a database
- Generation reports that take 3+ seconds to create
- Triggering workflows and/or seding webhook notifications
- Powering up/ powering down additional virtual machines for handling load
- Offloading any long-running tasks

## Basic setup

`Redis` server Naturally, we need a redis server running:

> redis-server

##### settings.py
    
    # Configures Redis as the datastore between Django + Celery
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")

    # Save Celery task results in redis db
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")

##### celery.py

    import os
    from celery import Celery

    # set the default Django settings module for the 'celery' program.
    # this is also used in manage.py
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    
    app = Celery('core')

    # Using a string here means the worker don't have to serialize
    # the configuration object to child processes.
    # - namespace='CELERY' means all celery-related configuration keys
    #   should have a `CELERY_` prefix.
    app.config_from_object('django.conf:settings', namespace='CELERY')

    # Load task modules from all registered Django app configs.
    app.autodiscover_tasks()
    
##### Update root config `__init__.py`
    
    from .celery import app as celery_app
    
    __all__ = ('celery_app',)

#### Run Celery
> celery -A core worker -l INFO
- `celery` is the CLI command
- `-A core` references the django configuration folder `core` where `celery.py` lives.
- `worker` means our tasks offloader is running
- `l INFO` will provide a list of all registered tasks as well as more verbose output on tasks run.



#### app/tasks.py
    import random
    from celery import shared_task
    
    @shared_task
    def add(x, y):
        # Celery recognizes this as the 'app.tasks.add' task
        # the name is purposefully omitted here.
        return x + y

    @shared_task(name='multiply_two_numbers')
    def mul(x, y):
        # Celery recognizes this as the 'multiple_two_numbers' task
        total = x * (y * random.randint(3, 100))
        return total

### refers: 
 - https://docs.docker.com/engine/reference/commandline/compose_run/
 - https://docs.celeryq.dev/en/latest/userguide/periodic-tasks.html
 - https://www.codingforentrepreneurs.com/blog/celery-redis-django/
 - https://www.youtube.com/watch?v=oBQxFn1CDno