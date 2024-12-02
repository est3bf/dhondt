#!/usr/bin/python3
import logging

from flask import Flask
from flask_smorest import Api

from dhondt.web.api.config import BaseConfig
import dhondt.web.api.api as api

app = Flask(__name__)

app.config.from_object(BaseConfig)

dhondt_api = Api(app)

logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Logger de la aplicación
logger = logging.getLogger(__name__)

# register api
dhondt_api.register_blueprint(api.blueprint)
