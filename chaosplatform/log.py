import logging
import logging.config
from logging import StreamHandler
import pkgutil
from typing import Any, Dict

from flask import Flask
from requestlogger import ApacheFormatter, WSGILogger
import simplejson as json

__all__ = ["configure_logger", "http_requests_logger"]

logger = logging.getLogger("chaosplatform")


def configure_logger(log_conf_path: str, config: Dict[str, Any]):
    log_conf = json.loads(pkgutil.get_data('chaosplatform', 'logging.json'))
    logging.config.dictConfig(log_conf)
    if config["debug"]:
        [h.setLevel(logging.DEBUG) for h in logger.handlers]
        logger.setLevel(logging.DEBUG)
    logger.debug("Logger configured")


def http_requests_logger(app: Flask,
                         stream_handler: StreamHandler = None) -> WSGILogger:
    if not stream_handler:
        stream_handler = StreamHandler()
    return WSGILogger(
        app.wsgi_app, [stream_handler], ApacheFormatter(), propagate=False)
