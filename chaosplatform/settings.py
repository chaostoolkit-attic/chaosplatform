# -*- coding: utf-8 -*-
from typing import Any, Dict

import cherrypy
import toml

__all__ = ["load_settings"]


def load_settings(toml_path: str) -> Dict[str, Any]:
    """
    """
    config = toml.load(toml_path)
    debug = config["chaosplatform"]["debug"]
    server_addr = config["chaosplatform"]["http"]["address"]
    host, port = server_addr.rsplit(":", 1)

    cherrypy.engine.unsubscribe('graceful', cherrypy.log.reopen_files)
    cherrypy.config.update({
        'server.socket_host': host,
        'server.socket_port': int(port),
        'engine.autoreload.on': False,
        'log.screen': debug,
        'log.access_file': '',
        'log.error_file': '',
        'environment': config["chaosplatform"].get("environment", "")
    })

    if "proxy" in config["chaosplatform"]["http"]:
        cherrypy.config.update({
            'tools.proxy.on': True,
            'tools.proxy.base': config["chaosplatform"]["http"]["proxy"]
        })

    return config["chaosplatform"]
