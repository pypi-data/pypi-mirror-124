# About
This package provides services for django applications. The servitin service is an asynchronous standalone application.


# Installation
```shell
pip install servitin
```

# Howto
Add ```servitin``` to ```settings.INSTALLED_APPS```

Make sure you have ```LOGGING``` settings in your project - servitin needs this.

Let's say you have a django app ```myapp```.

Make ```myapp``` a servitin service by adding the line ```is_servitin = True``` in ```myapp/apps.py```:
```python
from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
    is_servitin = True
```

Create file ```myapp/servitin.py```:

```python
from servitin.base import BaseService

class Service(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.info(f"Myapp service ready.")
```

(Not necessary) Give the version ```myapp```, write in the file ```myapp/__init__.py```:
```python
__version__ = '1.0'
```

Start service:
```shell
./manage.py run_servitin
```

If all is ok you will see in the log ```Myapp service ready.```

# Logging
To configure the built-in logger for each service, Servitin looks for a logger named ```servitin_myservice_logger``` for the ```myservice``` app, 
similarly for the ```my_other_service``` app it will look for ```servitin_my_other_service_logger```.

Buil-in logger is used like this:
```python
self.log.info(f"Myapp service ready.")
```
in the example above

# Request handling
Edit ```myapp/servitin.py``` to make the service as the ZeroMQ server:

```python
from servitin.base import BaseService
from servitin.lib.zmq.server import ZMQServer

class Service(ZMQServer, BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.info(f"Myapp service ready.")
```

Create ```myapp/settings.py```:

```python
from django.conf import settings

settings.SERVITIN_MYAPP_ZMQ = getattr(settings, 'SERVITIN_MYAPP_ZMQ', {
    'BIND_ADDRESS': 'tcp://*:5555',
    'CONNECT_ADDRESS': 'tcp://127.0.0.1:5555',
    'SECRET': ''
})
```

Create file ```myapp/zmq.py```:

```python
import asyncio
from servitin.lib.zmq.server import zmq, Response
from asgiref.sync import sync_to_async
from django.core import serializers
from django.contrib.auth.models import User
from servitin.utils import serializable

@zmq
async def get_users(request):
    order_by = request.data['order_by']
    # use built-in logger
    request.log.info(f'request order: {order_by}', name='@get_users')

    def get_data():
        # data with datetime objects, so it no serializable
        data = serializers.serialize('python', User.objects.all().order_by(order_by), fields=('username', 'date_joined'))
        # so make it serializable (you can use your own serializer) 
        return serializable(data)
    
    return Response(request, await sync_to_async(get_data)())


@zmq
async def heavy_task(request):
    """ emulate heavy task endpoint for timeout test """

    await asyncio.sleep(5)
    request.log.info(f'data: {request.data}', id=request.request_id, name='@heavy_task')
    return Response(request, f'complete: {request.data}')
```

Here we have created two endpoints: ```get_users```, ```heavy_task```.
The service is ready to handle requests, let's test it.

Create django management command ```myapp/management/commands/test_myapp_service.py```:

```python
import asyncio
from django.core.management import BaseCommand
from servitin.lib.zmq.client import Servitin
import myapp.settings  # import our service settings


class Command(BaseCommand):
    def handle(self, *args, **options):

        async def do():
            async with Servitin('myapp').connect() as my_service:
                print(await my_service.get_users({'order_by': 'username'}))

        asyncio.run(do())

```
In this example servitin client configured via ```myapp/settings.py```.

Run it:
```shell
./manage.py test_myapp_service
```

# Calls

It is also possible to use the servitin client outside of django.

Create file ```test_calls.py```:

```python
from servitin.lib.zmq.client import Servitin
import asyncio


loop = asyncio.get_event_loop()
params = {'connect': 'tcp://127.0.0.1:5555', 'secret': ''}


# ASYNC CALLS

async def do():
    # manual close connection
    my_service = Servitin(**params)
    results = await asyncio.gather(*[
        my_service.get_users({'order_by': 'username'}),
        my_service.get_users({'order_by': 'id'})
    ])
    print(results)
    my_service.close()  # close connection

    # auto close connection via context manager
    async with Servitin(**params).connect() as my_service:
        print(await my_service.get_users({'order_by': 'username'}))

    # timeout
    # you can specify timeout by passing it to Servitin():
    # async with Servitin(connect='tcp://127.0.0.1:5555', secret='', timeout=1).connect() as my_service:
    async with Servitin(**params).connect() as my_service:
        try:
            # or pass it directly in call
            print(await my_service.heavy_task({'data': 'context manager, timeout call'}, timeout=1))
        except asyncio.TimeoutError as e:
            print(e.__repr__())


loop.run_until_complete(do())


# SYNC CALLS

params = {'connect': 'tcp://127.0.0.1:5555', 'secret': '', 'async_mode': False}

# manual
my_service = Servitin(**params)
print(my_service.get_users({'order_by': 'username'}))
my_service.close()

# via context manager
with Servitin(**params).sync_connect() as my_service:
    print(my_service.get_users({'order_by': 'username'}))


loop.close()

```