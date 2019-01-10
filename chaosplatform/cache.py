from flask import Flask
from flask_caching import Cache

__all__ = ["setup_cache"]


def setup_cache(app: Flask) -> Cache:
    """
    Initialize the application's cache.
    """
    return Cache(app, config=app.config)
