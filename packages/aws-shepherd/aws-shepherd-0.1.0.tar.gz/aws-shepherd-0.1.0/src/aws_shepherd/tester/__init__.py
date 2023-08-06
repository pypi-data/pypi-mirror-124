import logging

log = logging.getLogger(__name__)


def handler(event, context):
    log.info(f'Got event: [{event}]')
