
# -*- coding: utf-8 -*-
from flask import Blueprint,  Flask
from flask_login import login_required

__all__ = ["register_views"]

plane = Blueprint("control_plane", __name__)


def register_views(app: Flask, prefix: str = '/'):
    prefix = prefix.rstrip("/")
    app.register_blueprint(plane, url_prefix="{}/".format(prefix))


@plane.route('')
@login_required
def index():
    return "hello"
