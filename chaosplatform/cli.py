import click

from . import __version__
from .log import configure_logger
from .server import run_forever
from .settings import load_settings


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


@cli.command()
@click.option('--config',
              type=click.Path(exists=True, readable=True, resolve_path=True),
              help='Configuration TOML file.')
@click.option('--logger-config',
              type=click.Path(exists=False, readable=True, resolve_path=True),
              help='Python logger JSON definition.')
@click.option('--with-ui', is_flag=True, default=False, show_default=True,
              help='Run the UI')
def run(config: str = None, logger_config: str = None, with_ui: bool = False):
    """
    Runs the application.
    """
    config = load_settings(config)
    config["ui"] = with_ui
    configure_logger(logger_config, config)
    run_forever(config)
