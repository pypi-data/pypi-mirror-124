import logging
import os
from functools import lru_cache
from http.client import HTTPConnection, HTTPSConnection
from json import JSONEncoder, JSONDecoder
import socket
from urllib.parse import urlparse, ParseResult


logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)


def _target() -> ParseResult:
    target = os.environ.get('NGROK_URL')

    if target is None:
        raise Exception('Environment variables for NGROK_URL is not set')

    log.debug(f'Target proxy will be: [{target}]')

    return urlparse(target)


def handler(event, context):
    log.debug(f'Proxying request [{event}]')
    cxn = (HTTPSConnection if _target().scheme == 'https' else HTTPConnection)(_target().hostname, _target().port)
    try:
        log.debug('Requesting')
        cxn.request(
            'POST', '/lambda',
            JSONEncoder().encode(dict(event=event, context={}, env_vars={k: v for k, v in os.environ.items()
                                                                         if 'AWS_XRAY' not in k})),
            headers={'Content-type': 'application/json'})

        log.debug('Responsing')
        resp = cxn.getresponse()
        if resp.status != 200:
            log.error(f'Response failed: [{resp.status}]')
            raise Exception(resp.read().decode('utf8'))
        else:
            result = JSONDecoder().decode(resp.read().decode('utf8'))
            return result.get('data', None)
    except Exception as e:
        log.error(f'Operation failed: [{e}]')
        raise

