import logging
import os
from logging import StreamHandler
from typing import Any, Dict
from unittest.mock import MagicMock

from requestlogger import ApacheFormatter, WSGILogger

from chaosplatform.log import clean_logger, configure_logger, \
    http_requests_logger


def test_configure_logger_with_embedded_config(config: Dict[str, Any]):
    logger = logging.getLogger("chaosplatform")
    assert len(logger.handlers) == 0

    try:
        configure_logger(None, config)
        assert logger.propagate is False
        assert logger.level == logging.INFO
        assert len(logger.handlers) == 1
        h = logger.handlers[0]
        assert isinstance(h, StreamHandler)
        assert h.level == logging.INFO
    finally:
        clean_logger()



def test_override_log_level(config: Dict[str, Any]):
    config = config.copy()
    config["debug"] = True

    logger = logging.getLogger("chaosplatform")
    assert len(logger.handlers) == 0

    try:
        configure_logger(None, config)
        assert logger.propagate is False
        assert logger.level == logging.DEBUG

        assert len(logger.handlers) == 1
        h = logger.handlers[0]
        assert isinstance(h, StreamHandler)
        assert h.level == logging.DEBUG
    finally:
        clean_logger()


def test_configure_logger_with_specific_config(config: Dict[str, Any]):
    logger = logging.getLogger("chaosplatform")
    assert len(logger.handlers) == 0

    try:
        p = os.path.join(
            os.path.dirname(__file__), "fixtures", "dummy-logging.json")
        configure_logger(p, config)
        assert logger.propagate is False
        assert logger.level == logging.ERROR
        assert len(logger.handlers) == 1
        h = logger.handlers[0]
        assert isinstance(h, StreamHandler)
        assert h.level == logging.ERROR
    finally:
        clean_logger()


def test_http_requests_logger():
    app = MagicMock()
    wsgi_logger = http_requests_logger(app)
    assert isinstance(wsgi_logger, WSGILogger)