"""
Will run in a container in Docker Compose and ensure that everything
is properly set up (like in the cloud) before we start interacting with the system.
"""

import asyncio
import logging
import typing
from typing import List

from aiohttp import web
import env_var_config

from . import waiters


ENV_READY_FLAG = 'is Compose environment ready?'

_log = logging.getLogger(__name__)


def run_status_app():
    logging.basicConfig(level=logging.INFO)

    app = web.Application()
    app[ENV_READY_FLAG] = False
    app.on_startup.append(wait_for_systems)
    app.router.add_route('GET', '/', is_env_ready)

    web.run_app(app, port=_get_config().port)


class Config(typing.NamedTuple):
    port: int
    redis_hostnames: str
    urls: str


async def is_env_ready(request: web.Request):
    """Responds with 503 until all the services we wait for come online. Then it returns 204.
    """
    if request.app[ENV_READY_FLAG]:
        return web.HTTPNoContent()
    else:
        return web.HTTPServiceUnavailable(text="The environment isn't ready yet.")


async def wait_for_systems(app):
    config = _get_config()
    url_waits = [waiters.wait_for_url(url) for url in _list_split(config.urls)]
    redis_waits = [waiters.wait_for_redis(host) for host in _list_split(config.redis_hostnames)]

    _log.info('Awaiting for external systems...')
    # More functions could be added here.
    await asyncio.gather(
        *url_waits,
        *redis_waits,
    )
    app[ENV_READY_FLAG] = True
    _log.info('All systems ready.')


def _get_config() -> Config:
    return env_var_config.gather_config_for_class(Config)


def _list_split(list_string: str) -> List[str]:
    """Parses a string containing commas into a list of strings.
    """
    return [element.strip() for element in list_string.split(',')]


if __name__ == '__main__':
    run_status_app()
