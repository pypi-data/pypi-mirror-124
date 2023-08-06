import asyncio
import json
import aiozmq.rpc
import zmq
from jose import jwt
from async_timeout import timeout as atimeout
from contextlib import asynccontextmanager, contextmanager


try:
    from django.conf import settings
    settings.DEBUG
except Exception:
    settings = None


class ValidationError(Exception):
    pass


class ImproperlyConfigured(Exception):
    pass


class Servitin:
    def __init__(self, service_name=None, async_mode=True, connect=None, secret=None, loop=None, timeout=None):
        self.loop = loop if loop else asyncio.get_event_loop()
        self.connection = None
        self.async_mode = async_mode
        self.timeout = timeout

        if settings:
            try:
                self.service_name = service_name
                self.settings = getattr(settings, f"SERVITIN_{self.service_name.upper()}_ZMQ", None)
                self.conn_str = self.settings['CONNECT_ADDRESS']
                self.secret = self.settings['SECRET']
            except Exception as e:
                raise ImproperlyConfigured(f'Servitin {self.service_name}.settings error: {e.__repr__()}')
        else:
            self.conn_str = connect
            self.secret = secret

        if self.conn_str is None:
            raise ImproperlyConfigured('No connection string passed')

        if self.secret is None:
            raise ImproperlyConfigured('No secret string passed')

    async def _connect(self):
        try:
            self.connection = await aiozmq.rpc.connect_rpc(connect=self.conn_str, timeout=self.timeout)
            self.connection.transport.setsockopt(zmq.LINGER, 0)
        except Exception as e:
            raise Exception(f"Connect to {self.conn_str} error: {e.__repr__()}")

    def close(self):
        self.connection.close()

    async def request(self, endpoint, data, timeout=10):
        if not self.connection:
            await self._connect()

        data = {} if not data else data
        data = jwt.encode(data, self.secret, algorithm='HS256')

        with atimeout(timeout):
            resp = await self.connection.call.endpoint(endpoint, data)

        response = json.loads(resp)

        if response['error'] == 'ValidationError':
            raise ValidationError(response['data'])
        return response

    def __getattr__(self, endpoint):
        async def async_call(data, **kwargs):
            return await self.request(endpoint, data, **kwargs)

        def sync_call(data, **kwargs):
            return self.loop.run_until_complete(self.request(endpoint, data, **kwargs))

        return async_call if self.async_mode else sync_call

    @asynccontextmanager
    async def connect(self):
        try:
            await self._connect()
            yield self
        finally:
            self.close()

    @contextmanager
    def sync_connect(self):
        try:
            self.loop.run_until_complete(self._connect())
            yield self
        finally:
            self.close()