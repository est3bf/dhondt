#!/usr/bin/env python3

import shlex
from subprocess import check_output, CalledProcessError
from setuptools import setup, find_packages


def git_to_pep440(git_version):
    if "-" not in git_version:
        return git_version

    sep = git_version.index("-")
    version = git_version[:sep] + "+dev" + git_version[sep + 1 :].replace("-", ".")
    return version


def git_version():
    cmd = "git describe --tags --always --dirty --match v[0-9]*"
    try:
        git_version = check_output(shlex.split(cmd)).decode("utf-8").strip()[1:]
    except CalledProcessError as e:
        raise Exception("Could not get git version") from e
    return git_to_pep440(git_version)


setup(
    name="dhondt-method",
    version=git_version(),
    description="",
    long_description="",
    url="http://github/estebanf/dhondt",
    author="Esteban Faye",
    license="",
    author_email="est3ban.faye@gmail.com",
    packages=["dhondt"]
    + [f"dhondt.{sub_pkg}" for sub_pkg in find_packages(where="src")],
    package_dir={
        "dhondt": "src",
    },
    classifiers=[
        "Development Status :: 1 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: Linux",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    install_requires=[
        "jinja2",
        "flask",
        "flask-smorest",
        "psycopg2",
        "alembic",
        "sqlalchemy",
        "sqlalchemy_utils",
        "pyyaml",
    ],
)
