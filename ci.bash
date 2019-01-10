#!/bin/bash
set -eo pipefail

function lint () {
    echo "Checking the code syntax"
    pylama chaosplatform
}

function build () {
    echo "Building the package"
    python setup.py build
}

function run-test () {
    echo "Running the tests"
    python setup.py test
}

function release () {
    echo "Releasing the package"
    python setup.py sdist bdist_wheel

    echo "Publishing to PyPI"
    pip install twine
    twine upload dist/* -u ${PYPI_USER_NAME} -p ${PYPI_PWD}
}

function main () {
    lint || return 1
    build || return 1
    run-test || return 1

    if [[ $TRAVIS_PYTHON_VERSION =~ ^3\.6+$ ]]; then
        if [[ $TRAVIS_TAG =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo "Releasing tag $TRAVIS_TAG with Python $TRAVIS_PYTHON_VERSION"
            release || return 1
        fi
    fi
}

main "$@" || exit 1
exit 0