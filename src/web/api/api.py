import logging

from flask import abort, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError

logger = logging.getLogger(__name__)

blueprint = Blueprint("dhondt", __name__, description="D'hondt method API")


########################
# Configurations
########################
@blueprint.route("/dhondt/v1/districts")
class DistrictsRoute(MethodView):
    def get(self):
        pass


@blueprint.route("/dhondt/v1/districts/<districtId>")
class DistrictRoute(MethodView):
    def get(self, districtId):
        pass


@blueprint.route("/dhondt/v1/districts/<districtId>/political-party-lists")
class PoliticalPartyListsRoute(MethodView):
    def get(self, districtId):
        pass

    def post(self, payload, districtId):
        pass


@blueprint.route("/dhondt/v1/districts/<districtId>/political-party-lists/<pplistId>")
class PoliticalPartyListRoute(MethodView):
    def get(self, districtId, pplistId):
        pass

    def put(self, parameters, districtId, pplistId):
        pass


@blueprint.route("/dhondt/v1/districts/<districtId>/scrutinies")
class ScrutiniesRoute(MethodView):
    def get(self, districtId):
        pass

    def post(self, payload, districtId):
        pass


@blueprint.route("/dhondt/v1/districts/<districtId>/scrutinies/<scrutinyId>")
class ScrutinyRoute(MethodView):
    def get(self, districtId, scrutinyId):
        pass


########################
# Upgrading votes
########################
@blueprint.route(
    "/dhondt/v1/districts/<districtId>/political-party-lists/<pplistId>/vote",
    methods=["PUT"],
)
def upgrade_vote(parameters, districtId, pplistId):
    pass


########################
# Seats Result
########################
@blueprint.route(
    "/dhondt/v1/districts/<districtId>/scrutinies/<scrutinyId>/seats-status"
)
class CalculateSeatsRoute(MethodView):
    def get(self, parameters, districtId, scrutinyId):
        pass

    def post(self, districtId, scrutinyId):
        pass
