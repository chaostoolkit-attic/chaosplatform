# -*- coding: utf-8 -*-
from copy import deepcopy
from typing import Any, Dict

import cherrypy
import toml

__all__ = ["load_settings"]


def load_settings(toml_path: str) -> Dict[str, Any]:
    """
    """
    config = toml.load(toml_path)
    populate_config_from_root(config)

    debug = config["chaosplatform"]["debug"]
    server_addr = config["chaosplatform"]["http"]["address"]
    host, port = server_addr.rsplit(":", 1)
    default_cherrypy_env = "" if debug else "production"

    cherrypy_config = config["chaosplatform"]["http"]["cherrypy"]
    cherrypy.engine.unsubscribe('graceful', cherrypy.log.reopen_files)
    cherrypy.config.update({
        'server.socket_host': host,
        'server.socket_port': int(port),
        'engine.autoreload.on': False,
        'log.screen': debug,
        'log.access_file': cherrypy_config.get("access_file", ""),
        'log.error_file': cherrypy_config.get("error_file", ""),
        'environment': cherrypy_config.get(
            "environment", default_cherrypy_env)
    })

    if "proxy" in config["chaosplatform"]["http"]:
        cherrypy.config.update({
            'tools.proxy.on': True,
            'tools.proxy.base': config["chaosplatform"]["http"]["proxy"]
        })

    return config["chaosplatform"]


def populate_config_from_root(config: Dict[str, Any]):
    """
    Populate all global configuration settings down to each service
    when they aren't set yet.
    """
    root_config = config.get("chaosplatform")
    debug = root_config.get("debug", False)

    root_config["http"].setdefault("debug", debug)
    root_config["db"].setdefault("debug", debug)
    root_config["grpc"].setdefault("debug", debug)

    for svc in ('account', 'auth', 'experiment', 'scheduling', 'scheduler'):
        svc_config = root_config.get(svc)
        if not svc_config:
            svc_config = {}
            root_config[svc] = svc_config

        svc_config.setdefault("debug", debug)

        jwt_config = deepcopy(root_config['jwt'])
        svc_config['jwt'] = jwt_config

        cache_config = deepcopy(root_config['cache'])
        svc_config['cache'] = cache_config

        http_config = root_config.get("http")
        if "http" not in svc_config:
            svc_config["http"] = {}

        svc_config["http"].setdefault("debug", debug)
        svc_config["http"].setdefault("address", http_config.get("address"))
        svc_config["http"].setdefault("proxy", http_config.get("proxy"))
        svc_config["http"].setdefault(
            "secret_key", http_config.get("secret_key"))
        svc_config["http"].setdefault(
            "environment", http_config.get("environment", "production"))

        db_config = root_config.get("db")
        if "db" not in svc_config:
            svc_config["db"] = {}

        svc_config["db"].setdefault("debug", debug)
        svc_config["db"].setdefault("uri", db_config.get("uri"))

        grpc_config = root_config.get("grpc")
        if "grpc" not in svc_config:
            svc_config["grpc"] = {}

        svc_config["grpc"].setdefault("debug", debug)
        svc_config["grpc"].setdefault("address", grpc_config.get("address"))
