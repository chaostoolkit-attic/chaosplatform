import logging
import logging.config
from logging import StreamHandler
import pkgutil
from typing import Any, Dict

from flask import Flask
from requestlogger import ApacheFormatter, WSGILogger
import simplejson as json

__all__ = ["clean_logger", "configure_logger", "http_requests_logger"]

logger = logging.getLogger("chaosplatform")


def configure_logger(log_conf_path: str, config: Dict[str, Any]):
    if log_conf_path:
        with open(log_conf_path) as f:
            log_conf = json.load(f)
    else:
        log_conf = json.loads(
            pkgutil.get_data('chaosplatform', 'logging.json'))
    logging.config.dictConfig(log_conf)
    if config["debug"]:
        [h.setLevel(logging.DEBUG) for h in logger.handlers]
        logger.setLevel(logging.DEBUG)
    logger.debug("Logger configured")


def clean_logger():
    """
    Clean all handlers attached to the logger
    """
    for h in logger.handlers[:]:
        logger.removeHandler(h)


def http_requests_logger(app: Flask,
                         stream_handler: StreamHandler = None) -> WSGILogger:
    if not stream_handler:
        stream_handler = StreamHandler()
    return WSGILogger(
        app.wsgi_app, [stream_handler], ApacheFormatter(), propagate=False)
