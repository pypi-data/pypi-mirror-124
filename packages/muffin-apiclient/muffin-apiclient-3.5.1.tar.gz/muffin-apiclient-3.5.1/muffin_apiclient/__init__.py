"""Support session with Muffin framework."""

import typing as t

from muffin import Application
from muffin.plugins import BasePlugin

from apiclient import APIClient


__version__ = "3.5.1"
__project__ = "muffin-apiclient"
__author__ = "Kirill Klenov <horneds@gmail.com>"
__license__ = "MIT"


T = t.TypeVar('T', bound=t.Callable)


class Plugin(BasePlugin):

    """Make external API requests."""

    # Can be customized on setup
    name = 'apiclient'
    root_url: t.Optional[str] = None
    timeout: t.Optional[int] = None

    defaults: t.Dict = {

        # Root URL (https://api.github.com)
        'root_url': None,

        # APIClient Backend (httpx|aiohttp)
        'backend_type': 'httpx',
        'backend_options': {},

        # Default client timeout
        'timeout': None,

        'raise_for_status': True,
        'read_response_body': True,
        'parse_response_body': True,

        # Client defaults (auth, headers)
        'client_defaults': {},
    }

    client = None

    def setup(self, app: Application, **options):
        """Setup API Client."""
        super().setup(app, **options)
        self.cfg.update(
            root_url=self.cfg.root_url or self.root_url,
            timeout=self.cfg.timeout or self.timeout,
        )
        self.client = APIClient(
            self.cfg.root_url, timeout=self.cfg.timeout,
            backend_type=self.cfg.backend_type,
            backend_options=self.cfg.backend_options,
            raise_for_status=self.cfg.raise_for_status,
            read_response_body=self.cfg.read_response_body,
            parse_response_body=self.cfg.parse_response_body,
            **self.cfg.client_defaults
        )
        self.api = self.client.api

    async def startup(self):
        """Startup self client."""
        await self.client.startup()

    async def shutdown(self):
        """Shutdown self client."""
        await self.client.shutdown()

    def client_middleware(self, fn: T) -> T:
        """Register a middleware."""
        client = t.cast(APIClient, self.client)
        return client.middleware(fn)

    def request(self, *args, **kwargs) -> t.Awaitable:
        """Make a request."""
        client = t.cast(APIClient, self.client)
        return client.request(*args, **kwargs)
