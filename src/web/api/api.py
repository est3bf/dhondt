import logging

from flask_smorest import Blueprint

logger = logging.getLogger(__name__)

blueprint = Blueprint("dhondt", __name__, description="D'hondt method API")
