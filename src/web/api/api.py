import logging

from flask import abort, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError

from dhondt.db.controller import get_db_session
from dhondt.db.dhondt_repository import DhondtRepository
from dhondt.dhondt_service.dhondt_service import DhondtService
from dhondt.dhondt_service.exceptions import (
    DistrictsNotFoundError,
    PoliticalPartyListsNotFoundError,
    ScrutinyNotFoundError,
    SeatsResultsNotFoundError,
)

from dhondt.web.api.schemas import (
    CreatePoliticalPartyList,
    PoliticalPartyList,
    GetPoliticalPartyLists,
    District,
    GetDistricts,
    CreateScrutiny,
    Scrutiny,
    GetScrutinies,
    SeatsResults,
    TotalSeatsResults,
    GetDistrictsParameters,
    GetScrutiniesParameters,
    UpgradeVoteParameters,
    GetResultsParameters,
)


logger = logging.getLogger(__name__)

blueprint = Blueprint("dhondt", __name__, description="D'hondt method API")


########################
# Configurations
########################
@blueprint.route("/dhondt/v1/districts")
class DistrictsRoute(MethodView):
    @blueprint.arguments(GetDistrictsParameters, location="query")
    @blueprint.response(status_code=200, schema=GetDistricts)
    def get(self, parameters):
        scrutiny_date = parameters.get("scrutinyDate")
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.get_districts(scrutiny_date=scrutiny_date)
            errors = GetDistricts().validate(results)
            if errors:
                raise ValidationError(errors)
            return jsonify(results)

        except DistrictsNotFoundError:
            detail = (
                f"District with scrutiny date {scrutiny_date}"
                if scrutiny_date
                else "Districts "
            )
            abort(404, description="{}not found!".format(detail))


@blueprint.route("/dhondt/v1/districts/<districtId>")
class DistrictRoute(MethodView):
    @blueprint.response(status_code=200, schema=District)
    def get(self, districtId):
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.get_districts(district_id=districtId)
            logger.info("A validar %s", results)
            errors = District().validate(results)
            if errors:
                raise ValidationError(errors)
            return jsonify(results)

        except DistrictsNotFoundError:
            abort(404, description=f"District with district id {districtId} not found!")


@blueprint.route("/dhondt/v1/districts/<districtId>/political-party-lists")
class PoliticalPartyListsRoute(MethodView):
    @blueprint.response(status_code=200, schema=GetPoliticalPartyLists)
    def get(self, districtId):
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.get_political_party_lists(
                    district_id=districtId
                )
            errors = GetPoliticalPartyLists().validate(results)
            if errors:
                raise ValidationError(errors)
            return jsonify(results)

        except PoliticalPartyListsNotFoundError:
            abort(
                404, description=f"Political Party Lists with {districtId=} not found!"
            )

    @blueprint.arguments(CreatePoliticalPartyList)
    @blueprint.response(status_code=201, schema=PoliticalPartyList)
    def post(self, payload, districtId):
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.create_political_party_list(
                    districtId=districtId, **payload
                )

            logger.debug(" Validating %s", results)
            errors = PoliticalPartyList().validate(results)
            if errors:
                raise ValidationError(errors)
            return jsonify(results)
        except DistrictsNotFoundError:
            abort(
                404,
                description="District Id {} not found!".format(
                    payload.get("districtId")
                ),
            )


@blueprint.route("/dhondt/v1/districts/<districtId>/political-party-lists/<pplistId>")
class PoliticalPartyListRoute(MethodView):
    @blueprint.response(status_code=200, schema=PoliticalPartyList)
    def get(self, districtId, pplistId):
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.get_political_party_lists(
                    district_id=districtId, pplist_id=pplistId
                )
            logger.info("A validar %s", results)
            errors = PoliticalPartyList().validate(results)
            if errors:
                raise ValidationError(errors)
            return jsonify(results)
        except PoliticalPartyListsNotFoundError:
            abort(
                404,
                description=(
                    f"Political Party Lists with district id {districtId} not found!"
                ),
            )

    @blueprint.arguments(CreatePoliticalPartyList)
    @blueprint.response(status_code=200, schema=PoliticalPartyList)
    def put(self, parameters, districtId, pplistId):
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.update_political_party_list(
                    district_id=districtId,
                    pplist_id=pplistId,
                    name=parameters.get("name"),
                    electors=parameters.get("electors"),
                )
            logger.info("A validar %s", results)
            errors = PoliticalPartyList().validate(results)
            if errors:
                raise ValidationError(errors)
            return jsonify(results)

        except PoliticalPartyListsNotFoundError:
            abort(
                404,
                description=(
                    f"Political Party Lists with district id {pplistId} not found!"
                ),
            )
        except DistrictsNotFoundError:
            id_district = parameters.get("districtId")
            abort(
                404,
                description=(
                    f"Political Party Lists with district id {id_district} not found!"
                ),
            )


@blueprint.route("/dhondt/v1/districts/<districtId>/scrutinies")
class ScrutiniesRoute(MethodView):
    @blueprint.arguments(GetScrutiniesParameters, location="query")
    @blueprint.response(status_code=200, schema=GetScrutinies)
    def get(self, parameters, districtId):
        scrutiny_date = parameters.get("scrutinyDate")
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.get_scrutinies(
                    district_id=districtId, scrutiny_date=scrutiny_date
                )
            errors = GetScrutinies().validate(results)
            if errors:
                raise ValidationError(errors)
            return jsonify(results)

        except ScrutinyNotFoundError:
            detail = f"Scrutiny with {districtId=} " + (
                f"and {scrutiny_date=} " if scrutiny_date else ""
            )
            abort(404, description="{}not found!".format(detail))

    @blueprint.arguments(CreateScrutiny)
    @blueprint.response(status_code=201, schema=Scrutiny)
    def post(self, payload, districtId):
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.create_scrutiny(
                    district_id=districtId, **payload
                )
            logger.debug(" Validating %s", results)
            errors = Scrutiny().validate(results)
            if errors:
                raise ValidationError(errors)
            return jsonify(results)

        except DistrictsNotFoundError:
            abort(
                404,
                description="District Id {} not found!".format(
                    payload.get("districtId")
                ),
            )


@blueprint.route("/dhondt/v1/districts/<districtId>/scrutinies/<scrutinyId>")
class ScrutinyRoute(MethodView):
    @blueprint.response(status_code=200, schema=Scrutiny)
    def get(self, districtId, scrutinyId):
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.get_scrutinies(
                    district_id=districtId, scrutiny_id=scrutinyId
                )
            logger.info("A validar %s", results)
            errors = Scrutiny().validate(results)
            if errors:
                raise ValidationError(errors)
            return jsonify(results)

        except ScrutinyNotFoundError:
            abort(404, description=f"Scrutiny with scrutiny id {scrutinyId} not found!")


########################
# Upgrading votes
########################
@blueprint.route(
    "/dhondt/v1/districts/<districtId>/political-party-lists/<pplistId>/vote",
    methods=["PUT"],
)
@blueprint.response(status_code=200, schema=PoliticalPartyList)
@blueprint.arguments(UpgradeVoteParameters)
def upgrade_vote(parameters, districtId, pplistId):
    try:
        with get_db_session() as session:
            repo = DhondtRepository(session)
            dhondt_service = DhondtService(repo)
            results = dhondt_service.update_vote(
                district_id=districtId,
                pplist_id=pplistId,
                votes=parameters.get("votes"),
            )
        logger.debug(" Validating %s", results)
        errors = PoliticalPartyList().validate(results)
        if errors:
            raise ValidationError(errors)
        return jsonify(results)

    except PoliticalPartyListsNotFoundError:
        abort(
            404,
            description=f"Political Party Lists with pplist id {pplistId} not found!",
        )


########################
# Seats Result
########################
@blueprint.route(
    "/dhondt/v1/districts/<districtId>/scrutinies/<scrutinyId>/seats-status"
)
class CalculateSeatsRoute(MethodView):
    @blueprint.response(status_code=200, schema=TotalSeatsResults)
    @blueprint.arguments(GetResultsParameters, location="query")
    def get(self, parameters, districtId, scrutinyId):
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.get_seats_results(
                    district_id=districtId,
                    scrutiny_id=scrutinyId,
                    limit=parameters.get("limit"),
                )
            logger.debug(" Validating %s", results)
            errors = TotalSeatsResults().validate(results)
            if errors:
                raise ValidationError(errors)
            return jsonify(results)

        except SeatsResultsNotFoundError:
            abort(
                404,
                description=(
                    f"Seats results not found for {districtId=} and {scrutinyId=}!"
                ),
            )

    @blueprint.response(status_code=200, schema=SeatsResults)
    def post(self, districtId, scrutinyId):
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.calculate_seats(
                    district_id=districtId, scrutiny_id=scrutinyId
                )
            logger.debug(" Validating %s", results)
            errors = SeatsResults().validate(results)
            if errors:
                raise ValidationError(errors)
            return jsonify(results)

        except ScrutinyNotFoundError:
            abort(
                404,
                description=(
                    f"Scrutiny with scrutiny {districtId=} and {scrutinyId} not found!"
                ),
            )
