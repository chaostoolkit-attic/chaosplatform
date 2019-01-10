import attr

__all__ = ["Services"]


@attr.s
class Services:
    auth: object = attr.ib(default=None)
    account: object = attr.ib(default=None)
    experiment: object = attr.ib(default=None)
    execution: object = attr.ib(default=None)
    scheduling: object = attr.ib(default=None)
    scheduler: object = attr.ib(default=None)
    worker: object = attr.ib(default=None)
