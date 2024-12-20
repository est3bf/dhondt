#!/usr/bin/python3
import os
from pathlib import Path
import yaml
import logging

from flask import Flask
from apispec import APISpec
from flask_smorest import Api

from dhondt.db.dhondt_repository import init_repository
from dhondt.web.api.config import BaseConfig
import dhondt.web.api.api as api
import dhondt.web.views as views


SPEC_NAMEFILE = "dhondt.yaml"

log_level = os.getenv("LOG_LEVEL", "").upper().strip()
if "DEBUG" == log_level:
    log_level = logging.DEBUG
elif "ERROR" == log_level:
    log_level = logging.ERROR
else:
    log_level = logging.INFO


logging.basicConfig(
    level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Logger de la aplicación
logger = logging.getLogger(__name__)


def create_app(test_config=None):
    """
    Create the application for API and view
    """
    app = Flask(__name__)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(BaseConfig)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    dhondt_api = Api(app)

    # register views
    for view_blueprint in views.blueprints:
        app.register_blueprint(view_blueprint)

    # register api
    dhondt_api.register_blueprint(api.blueprint)

    # load openapi specification
    api_spec = yaml.safe_load((Path(__file__).parent / SPEC_NAMEFILE).read_text())
    spec = APISpec(
        title=api_spec["info"]["title"],
        version=api_spec["info"]["version"],
        openapi_version=api_spec["openapi"],
    )
    spec.to_dict = lambda: api_spec
    dhondt_api.spec = spec
    return app


init_repository(os.getenv("__USE_MEMORY_DB"))
create_app()
