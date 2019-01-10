from datetime import timedelta
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

    app.config["SECRET_KEY"] = config["secret_key"]
    app.secret_key = app.config["SECRET_KEY"]

    app.config["JWT_SECRET_KEY"] = config["jwt"]["secret_key"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        minutes=config["jwt"]["access_token_expires"])

    # OAUTH2
    oauth2_config = config["oauth2"]
    oauth2_gh_cfg = oauth2_config["github"]
    app.config["GITHUB_OAUTH_CLIENT_ID"] = oauth2_gh_cfg["client_id"]
    app.config["GITHUB_OAUTH_CLIENT_SECRET"] = oauth2_gh_cfg["client_secret"]

    app.config["CACHE_TYPE"] = config["cache"].get("type", "simple")
    if app.config["CACHE_TYPE"] == "redis":
        app.config["CACHE_REDIS_HOST"] = config["cache"]["host"]
        app.config["CACHE_REDIS_PORT"] = config["cache"]["port"]

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
