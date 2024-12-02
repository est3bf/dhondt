#!/usr/bin/python3
import os
from pathlib import Path
import yaml
import logging

from flask import Flask
from apispec import APISpec
from flask_smorest import Api

from dhondt.web.api.config import BaseConfig
import dhondt.web.api.api as api


SPEC_NAMEFILE = "dhondt.yaml"


app = Flask(__name__)

app.config.from_object(BaseConfig)

dhondt_api = Api(app)


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
