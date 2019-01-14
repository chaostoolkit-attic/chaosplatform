import logging
from logging import StreamHandler
from typing import Any, Dict

import cherrypy
from flask import Flask
from requestlogger import ApacheFormatter, WSGILogger
from werkzeug.contrib.fixers import ProxyFix

from .auth import setup_jwt, setup_login

__all__ = ["cleanup_api", "create_api", "serve_api"]
logger = logging.getLogger("chaosplatform")


def create_api(config: Dict[str, Any]) -> Flask:
    """
    Create the Flask application and initialize its resources.
    """
    app = Flask(__name__)

    app.url_map.strict_slashes = False
    app.debug = config.get("debug", False)

    logger = logging.getLogger('flask.app')
    logger.propagate = False

    app.config["SECRET_KEY"] = config["http"]["secret_key"]
    app.secret_key = config["http"]["secret_key"]
    app.config["JWT_SECRET_KEY"] = config["jwt"]["secret_key"]
    app.config["SQLALCHEMY_DATABASE_URI"] = config["db"]["uri"]

    app.config["CACHE_TYPE"] = config["cache"].get("type", "simple")
    if app.config["CACHE_TYPE"] == "redis":
        redis_config = config["cache"]["redis"]
        app.config["CACHE_REDIS_HOST"] = redis_config.get("host")
        app.config["CACHE_REDIS_PORT"] = redis_config.get("port", 6379)
        app.config["CACHE_REDIS_DB"] = redis_config.get("db", 0)
        app.config["CACHE_REDIS_PASSWORD"] = redis_config.get("password")

    setup_jwt(app)
    setup_login(app, from_session=True, from_jwt=True)

    return app


def cleanup_api(settings: Dict[str, Any]):
    pass


def serve_api(app: Flask, mount_point: str = '/',
              log_handler: StreamHandler = None):
    log_handler = log_handler or logging.StreamHandler()
    app.wsgi_app = ProxyFix(app.wsgi_app)
    wsgiapp = WSGILogger(
        app.wsgi_app, [log_handler], ApacheFormatter(),
        propagate=False)
    cherrypy.tree.graft(wsgiapp, mount_point)
