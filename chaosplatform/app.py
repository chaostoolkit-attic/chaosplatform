import logging
from logging import StreamHandler
from typing import Any, Dict

import cherrypy
from flask import Flask
from requestlogger import ApacheFormatter, WSGILogger
from werkzeug.contrib.fixers import ProxyFix

from .auth import setup_login

__all__ = ["cleanup_app", "create_app", "serve_app"]
logger = logging.getLogger("chaosplatform")


def create_app(config: Dict[str, Any]) -> Flask:
    """
    Create the Flask application.
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

    # OAUTH2
    oauth2_config = config["auth"]["oauth2"]
    for backend in oauth2_config:
        provider = backend.upper()
        provider_config = oauth2_config[backend]

        app.config["_OAUTH_CLIENT_ID".format(provider)] = \
            provider_config["client_id"]
        app.config["_OAUTH_CLIENT_SECRET".format(provider)] = \
            provider_config["client_secret"]

    setup_login(app, from_session=True)

    return app


def cleanup_app(settings: Dict[str, Any]):
    pass


def serve_app(app: Flask, mount_point: str = '/',
              log_handler: StreamHandler = None):
    log_handler = log_handler or logging.StreamHandler()
    app.wsgi_app = ProxyFix(app.wsgi_app)
    wsgiapp = WSGILogger(
        app.wsgi_app, [log_handler], ApacheFormatter(),
        propagate=False)
    cherrypy.tree.graft(wsgiapp, mount_point)
