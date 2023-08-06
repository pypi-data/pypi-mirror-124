import importlib
import logging
import os
from functools import lru_cache
from typing import Tuple, Callable

from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)


def _module_and_handler() -> Tuple[str, str]:
    module = os.environ.get('SHEPHERD_MODULE', None)
    if module is None:
        raise Exception('Environment variable [SHEPHERD_MODULE] must be set')

    parts = module.split('.')
    return '.'.join(parts[:-1]), parts[-1]


@lru_cache
def _handler() -> Callable:
    module_name, handler_name = _module_and_handler()
    return getattr(importlib.import_module(module_name), handler_name)


def _config_env(env_vars: dict):
    for k, v in env_vars.items():
        if os.environ.get(k, None) is None:
            log.info(f'Setting environment variable: [{k}] = [{v}]')
            os.environ[k] = v


@app.post('/lambda')
def lambda_handler():
    log.debug('Received new request from lambda proxy')
    payload = request.json
    event, context, env_vars = payload['event'], payload['context'], payload['env_vars']
    _config_env(env_vars)

    try:
        result = _handler()(event, context)

        log.debug('Proxy request processing complete.')

        response = dict(status=200, message='OK')

        if result is not None:
            response['data'] = result

        return response
    except Exception as e:
        log.error('Lambda invocation failed')
        log.error(e)
        return dict(status=500, message=str(e))


if __name__ == '__main__':
    log.info('Starting local lambda listener')
    app.run(host='0.0.0.0', port=8888)

