import logging
from typing import Any, Dict, Tuple

from chaosplt_account.server import initialize_all as init_account, \
    release_all as release_account
from chaosplt_auth.server import initialize_all as init_auth, \
    release_all as release_auth
from chaosplt_experiment.server import initialize_all as init_experiment, \
    release_all as release_experiment
from chaosplt_scheduler.server import initialize_all as init_scheduler, \
    release_all as release_scheduler
from chaosplt_scheduling.server import initialize_all as init_scheduling, \
    release_all as release_scheduling
from chaosplt_grpc import create_grpc_server, start_grpc_server, \
    stop_grpc_server
import cherrypy
from flask import Flask
from grpc import Server as GRPCServer

from .app import create_app, cleanup_app, serve_app
from .api import create_api, cleanup_api, serve_api
from .cache import setup_cache
from .service import Services

__all__ = ["initialize_all", "release_all", "run_forever"]


def initialize_all(config: Dict[str, Any]) \
                   -> Tuple[Flask, Flask, Services, GRPCServer, Tuple, Tuple,
                            Tuple, Tuple, Tuple]:
    services = Services()

    access_log_handler = logging.StreamHandler()

    web_app = create_app(config)
    web_cache = setup_cache(web_app)

    api_app = create_api(config)
    api_cache = setup_cache(api_app)

    grpc_server = create_grpc_server(config["grpc"]["address"])
    start_grpc_server(grpc_server)

    account_resources = init_account(
        config["account"], web_app, api_app, services, grpc_server, web_cache,
        api_cache,
        web_mount_point="/account", api_mount_point="/account",
        access_log_handler=access_log_handler)
    auth_resources = init_auth(
        config["auth"], web_app, api_app, services, grpc_server, web_cache,
        api_cache,
        web_mount_point="/auth", api_mount_point="/auth",
        access_log_handler=access_log_handler)
    scheduler_resources = init_scheduler(
        config["scheduler"], services, grpc_server)
    scheduling_resources = init_scheduling(
        config["scheduling"], web_app, api_app, services, grpc_server,
        web_cache, api_cache,
        web_mount_point="/scheduling", api_mount_point="/scheduling",
        access_log_handler=access_log_handler)
    experiment_resources = init_experiment(
        config["experiment"], web_app, api_app, services, grpc_server,
        web_cache, api_cache,
        experiment_web_mount_point="/experi ment",
        experiment_api_mount_point="/experiments",
        execution_web_mount_point="/execution",
        execution_api_mount_point="/executions",
        access_log_handler=access_log_handler)

    serve_app(web_app, "/", access_log_handler)
    serve_api(api_app, "/api/v1", access_log_handler)

    return (
        web_app, api_app, services, grpc_server, auth_resources,
        account_resources, scheduler_resources, scheduling_resources,
        experiment_resources)


def release_all(services: Services, web_app: Flask, api_app: Flask,
                grpc_server: GRPCServer,
                auth_resources: Tuple, account_storage: Tuple,
                scheduler_resources: Tuple, scheduling_resources: Tuple,
                experiment_resources: Tuple):
    stop_grpc_server(grpc_server)
    cleanup_app(web_app)
    cleanup_api(api_app)
    release_scheduler(*scheduler_resources)
    release_account(*account_storage)
    release_auth(*auth_resources)
    release_scheduling(*scheduling_resources)
    release_experiment(*experiment_resources)


def run_forever(config: Dict[str, Any]):
    """
    Run and block until a signal is sent to the process.

    The application, services or gRPC server are all created and initialized
    when the application starts.
    """
    def run_stuff(config: Dict[str, Any]):
        resources = initialize_all(config)
        cherrypy.engine.subscribe(
            'stop', lambda: release_all(*resources),
            priority=20)

    cherrypy.engine.subscribe(
        'start', lambda: run_stuff(config), priority=80)

    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()
