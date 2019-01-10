from typing import Any, Dict

try:
    from chaosplt_relational_storage import initialize_storage
    from chaosplt_relational_storage import configure_storage
    from chaosplt_relational_storage import release_storage
    HAS_RELATIONAL_STORAGE_PACKAGE = True
except ImportError:
    HAS_RELATIONAL_STORAGE_PACKAGE = False

__all__ = ["get_storage_driver", "configure_storage_driver",
           "release_storage_driver"]


def get_storage_driver(provider: str, config: Dict[str, Any]) -> object:
    if provider == "native":
        if not HAS_RELATIONAL_STORAGE_PACKAGE:
            raise RuntimeError(
                "'chaosplatform-relational-storage' not installed")
        return initialize_storage(config)


def configure_storage_driver(provider: str, storage_driver: object):
    if provider == "native":
        if not HAS_RELATIONAL_STORAGE_PACKAGE:
            raise RuntimeError(
                "'chaosplatform-relational-storage' not installed")
        configure_storage(storage_driver)


def release_storage_driver(provider: str, storage_driver: object):
    if provider == "native":
        if not HAS_RELATIONAL_STORAGE_PACKAGE:
            raise RuntimeError(
                "'chaosplatform-relational-storage' not installed")
        return release_storage(storage_driver)
