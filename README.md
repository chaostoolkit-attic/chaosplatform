# Chaos Platform - Chaos Engineering Platform for Everyone

[![Version](https://img.shields.io/pypi/v/chaosplatform.svg)](https://img.shields.io/pypi/v/chaosplatform.svg)
[![License](https://img.shields.io/pypi/l/chaosplatform.svg)](https://img.shields.io/pypi/l/chaosplatform.svg)
[![StackOverflow](https://img.shields.io/badge/StackOverflow-ChaosPlatform-blue.svg)](https://stackoverflow.com/questions/tagged/chaosplatform+or+chaostoolkit)

[![Build Status](https://travis-ci.org/chaostoolkit/chaosplatform.svg?branch=master)](https://travis-ci.org/chaostoolkit/chaosplatform)
[![Python versions](https://img.shields.io/pypi/pyversions/chaosplatform.svg)](https://www.python.org/)

This is the [Chaos Platform][chaosplatform] main project.

[chaosplatform]: https://chaosplatform.org/

* WARNING*: This is an alpha release so expect things to get rocky and break for
now. We are heavily working on it although the API should remain stable. Please,
join the [slack][slack] to keep the discussion alive :) Thank you for being
patient with us!

[slack]: https://join.chaostoolkit.org/

## Install & Run

Documentation is being written so the instructions here are for the courageous.

* Install Python 3.6+. No promises are made for lower versions.
* Create a Python virtual environment
* Install pip
* Install Redis via a simple Docker image

```
$ docker run --rm --name redis -p 6379:6379 redis
```

* Install the Chaos Platform

```
$ pip install --pre -U chaosplatform
```

* Create a chaosplatform.toml configuration file:


```toml
[chaosplatform]
debug = false

    [chaosplatform.grpc]
    address = "0.0.0.0:50051"

    [chaosplatform.http]
    address = "0.0.0.0:8090"
    secret_key = ""

        [chaosplatform.http.cherrypy]
        environment = "production"
        proxy = "http://localhost:6080"

    [chaosplatform.cache]
    type = "simple"

        # Only set if type is set to "redis"
        # [chaosplatform.cache.redis]
        # host = "localhost"
        # port = 6379

    [chaosplatform.db]
    uri = "sqlite:///:memory"

    [chaosplatform.jwt]
    secret_key = ""
    public_key = ""
    algorithm = "HS256"
    identity_claim_key = "identity"
    user_claims_key = "user_claims"
    access_token_expires = 2592000
    refresh_token_expires = 31536000
    user_claims_in_refresh_token = false

    [chaosplatform.account]

    [chaosplatform.auth]
        [chaosplatform.auth.oauth2]
            [chaosplatform.auth.oauth2.github]
            client_id = ""
            client_secret = ""

        [chaosplatform.auth.grpc]
            [chaosplatform.auth.grpc.account]
            address = "0.0.0.0:50051"

    [chaosplatform.experiment]

    [chaosplatform.scheduling]
        [chaosplatform.scheduling.grpc]
            [chaosplatform.scheduling.grpc.scheduler]
            address = "0.0.0.0:50051"

    [chaosplatform.scheduler]
        [chaosplatform.scheduler.redis]
        host = "localhost"
        port = 6379
        queue = "chaosplatform"

        [chaosplatform.scheduler.job]
        platform_url = "http://127.0.0.1:6080"

        [chaosplatform.scheduler.worker]
        debug = false
        count = 3
        queue_name = "chaosplatform"
        worker_name = "chaosplatform-worker"
        add_random_suffix_to_worker_name = true
        worker_directory = "/tmp"

        [chaosplatform.scheduler.worker.redis]
        host = "localhost"
        port = 6379
```

* Run the Chaos Platform:

```
$ chaosplatform run --config=chaosplatform.toml
```

For now, the platform is GUI-less so needs to be called bia its [API][openapi].

[openapi]: https://github.com/chaostoolkit/chaosplatform-openapi

## Contribute

Contributors to this project are welcome as this is an open-source effort that
seeks [discussions][join] and continuous improvement.

[join]: https://join.chaostoolkit.org/

From a code perspective, if you wish to contribute, you will need to run a 
Python 3.5+ environment. Then, fork this repository and submit a PR. The
project cares for code readability and checks the code style to match best
practices defined in [PEP8][pep8]. Please also make sure you provide tests
whenever you submit a PR so we keep the code reliable.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Platform projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works