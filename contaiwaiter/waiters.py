import logging

import aiohttp
import aredis
import async_timeout
import tenacity

_log = logging.getLogger(__name__)

_retry_for_awhile = tenacity.retry(
    stop=tenacity.stop_after_delay(20),
    wait=tenacity.wait_fixed(0.1),
)


async def wait_for_url(url):
    """Waits until a URL response with a non-500 HTTP response.
    """
    _log.info(f'Waiting for {url} URL...')
    await _wait_for_url(url)


@_retry_for_awhile
async def _wait_for_url(url):
    async with async_timeout.timeout(1):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status >= 500:
                    raise UrlNotReadyError(f'{url} is not ready.')
                _log.info(f'URL {url} is ready.')


class UrlNotReadyError(Exception):
    """
    Raised when URL responded with a 500 status, or didn't respond with HTTP.
    """


async def wait_for_redis(hostname):
    _log.info(f'Waiting for Redis at {hostname} host...')
    await _wait_for_redis(hostname)


@_retry_for_awhile
async def _wait_for_redis(hostname):
    redis = aredis.StrictRedis(host=hostname)
    await redis.ping()
    _log.info(f'Redis at {hostname} is ready.')
