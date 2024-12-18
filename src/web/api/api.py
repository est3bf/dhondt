import logging
from copy import deepcopy

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
    PoliticalPartyListsAlreadyExist,
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
    ResourceId,
)


logger = logging.getLogger(__name__)

blueprint = Blueprint("dhondt", __name__, description="D'hondt method API")


@blueprint.errorhandler(404)
def resource_not_found_handler(e):
    detail = str(e.description) if e.description else "Internal Validation"
    return jsonify(code=404, status="Not Found", detail=detail), 404


@blueprint.errorhandler(400)
def bad_request_handler(e):
    return jsonify(code=400, status="Bad Request.", detail=str(e.description)), 400


@blueprint.errorhandler(422)
def unprocessable_handler(e):
    return (
        jsonify(code=422, status="Unprocessable Entity.", detail=str(e.description)),
        422,
    )


@blueprint.errorhandler(500)
def internal_error_handler(e):
    return (
        jsonify(code=500, status="Internal Error.", detail=str(e.description)),
        500,
    )


def _validate_resources(**kwargs):
    logger.debug(" Validating %s", kwargs)
    for _, val in kwargs.items():
        errors = ResourceId().validate({"id": val})
        if errors:
            abort(422, description=f"Validation error. Error: id {errors['id']}")


def _validate_result(schema, result):
    logger.debug(" Validating %s %s", schema, result)
    errors = schema().validate(result)
    if errors:
        abort(500, description=f"Validation error. Msg {errors}")


def _validate_scrutiny_result(result):
    res = deepcopy(result)
    res["votingDate"] = res["votingDate"].isoformat()
    res["scrutinyDate"] = res["scrutinyDate"].isoformat()
    logger.debug(" Validating scrutiny %s", res)
    errors = Scrutiny().validate(res)
    if errors:
        abort(500, description=f"Validation error. Msg {errors}")


def _validate_scrutinies_result(results):
    list_res = []
    for org_res in results["scrutinies"]:
        res = deepcopy(org_res)
        res["votingDate"] = res["votingDate"].isoformat()
        res["scrutinyDate"] = res["scrutinyDate"].isoformat()
        list_res.append(res)
    to_val = {"scrutinies": list_res}
    logger.debug(" Validating scrutinies %s", to_val)
    errors = GetScrutinies().validate(to_val)
    if errors:
        abort(500, description=f"Validation error. Msg {errors}")


def _validate_seats_result(result):
    res = deepcopy(result)
    res["calculationDate"] = res["calculationDate"].isoformat()
    logger.debug(" Validating seats_result %s", res)
    errors = SeatsResults().validate(res)
    if errors:
        abort(500, description=f"Validation error. Msg {errors}")


def _validate_total_seats_result(results):
    list_res = []
    for org_res in results["scrutinyResults"]:
        res = deepcopy(org_res)
        res["calculationDate"] = res["calculationDate"].isoformat()
        list_res.append(res)
    to_val = {"scrutinyResults": list_res}
    logger.debug(" Validating total reasult %s", to_val)
    errors = TotalSeatsResults().validate(to_val)
    if errors:
        abort(500, description=f"Validation error. Msg {errors}")


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
            _validate_result(GetDistricts, results)
            return results

        except DistrictsNotFoundError:
            detail = (
                f"District with scrutiny date {scrutiny_date}"
                if scrutiny_date
                else "Districts "
            )
            abort(404, description="{}not found!".format(detail))


@blueprint.route("/dhondt/v1/districts/<int:districtId>")
class DistrictRoute(MethodView):
    @blueprint.response(status_code=200, schema=District)
    def get(self, districtId):
        _validate_resources(districtId=districtId)
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.get_districts(district_id=districtId)

            _validate_result(District, results)
            return results

        except DistrictsNotFoundError:
            abort(404, description=f"District with district id {districtId} not found!")


@blueprint.route("/dhondt/v1/districts/<int:districtId>/political-party-lists")
class PoliticalPartyListsRoute(MethodView):
    @blueprint.response(status_code=200, schema=GetPoliticalPartyLists)
    def get(self, districtId):
        _validate_resources(districtId=districtId)
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.get_political_party_lists(
                    district_id=districtId
                )
            _validate_result(GetPoliticalPartyLists, results)
            return results

        except PoliticalPartyListsNotFoundError:
            abort(
                404, description=f"Political Party Lists with {districtId=} not found!"
            )

    @blueprint.arguments(CreatePoliticalPartyList)
    @blueprint.response(status_code=201, schema=PoliticalPartyList)
    def post(self, payload, districtId):
        _validate_resources(districtId=districtId)
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.create_political_party_list(
                    districtId=districtId, **payload
                )
            _validate_result(PoliticalPartyList, results)
            return results

        except DistrictsNotFoundError:
            abort(
                404,
                description="District Id {} not found!".format(
                    payload.get("districtId")
                ),
            )
        except PoliticalPartyListsAlreadyExist:
            abort(
                409,
                description=f"Political Party Lists with {districtId=} and {payload['name']=} already exists",
            )


@blueprint.route(
    "/dhondt/v1/districts/<int:districtId>/political-party-lists/<int:pplistId>"
)
class PoliticalPartyListRoute(MethodView):
    @blueprint.response(status_code=200, schema=PoliticalPartyList)
    def get(self, districtId, pplistId):
        _validate_resources(districtId=districtId, pplistId=pplistId)
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.get_political_party_lists(
                    district_id=districtId, pplist_id=pplistId
                )
            _validate_result(PoliticalPartyList, results)
            return results
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
        _validate_resources(districtId=districtId, pplistId=pplistId)
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
            _validate_result(PoliticalPartyList, results)
            return results

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
        except PoliticalPartyListsAlreadyExist:
            abort(
                409,
                description=f"Political Party Lists with {districtId=} and {parameters['name']=} already exists",
            )


@blueprint.route("/dhondt/v1/districts/<int:districtId>/scrutinies")
class ScrutiniesRoute(MethodView):
    @blueprint.arguments(GetScrutiniesParameters, location="query")
    @blueprint.response(status_code=200, schema=GetScrutinies)
    def get(self, parameters, districtId):
        _validate_resources(districtId=districtId)
        scrutiny_date = parameters.get("scrutinyDate")
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.get_scrutinies(
                    district_id=districtId, scrutiny_date=scrutiny_date
                )
            _validate_scrutinies_result(results)
            return results

        except ScrutinyNotFoundError:
            detail = f"Scrutiny with {districtId=} " + (
                f"and {scrutiny_date=} " if scrutiny_date else ""
            )
            abort(404, description="{}not found!".format(detail))

    @blueprint.arguments(CreateScrutiny)
    @blueprint.response(status_code=201, schema=Scrutiny)
    def post(self, payload, districtId):
        _validate_resources(districtId=districtId)
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.create_scrutiny(
                    district_id=districtId, **payload
                )
            _validate_scrutiny_result(results)
            return results

        except DistrictsNotFoundError:
            abort(
                404,
                description="District Id {} not found!".format(
                    payload.get("districtId")
                ),
            )


@blueprint.route("/dhondt/v1/districts/<int:districtId>/scrutinies/<int:scrutinyId>")
class ScrutinyRoute(MethodView):
    @blueprint.response(status_code=200, schema=Scrutiny)
    def get(self, districtId, scrutinyId):
        _validate_resources(districtId=districtId, scrutinyId=scrutinyId)
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.get_scrutinies(
                    district_id=districtId, scrutiny_id=scrutinyId
                )
            _validate_scrutiny_result(results)
            return results

        except ScrutinyNotFoundError:
            abort(404, description=f"Scrutiny with scrutiny id {scrutinyId} not found!")


########################
# Upgrading votes
########################
@blueprint.route(
    "/dhondt/v1/districts/<int:districtId>/political-party-lists/<int:pplistId>/vote",
    methods=["PUT"],
)
@blueprint.response(status_code=200, schema=PoliticalPartyList)
@blueprint.arguments(UpgradeVoteParameters)
def upgrade_vote(parameters, districtId, pplistId):
    _validate_resources(districtId=districtId, pplistId=pplistId)
    try:
        with get_db_session() as session:
            repo = DhondtRepository(session)
            dhondt_service = DhondtService(repo)
            results = dhondt_service.update_vote(
                district_id=districtId,
                pplist_id=pplistId,
                votes=parameters.get("votes"),
            )
        _validate_result(PoliticalPartyList, results)
        return results

    except PoliticalPartyListsNotFoundError:
        abort(
            404,
            description=f"Political Party Lists with pplist id {pplistId} not found!",
        )


########################
# Seats Result
########################
@blueprint.route(
    "/dhondt/v1/districts/<int:districtId>/scrutinies/<int:scrutinyId>/seats-status"
)
class CalculateSeatsRoute(MethodView):
    @blueprint.response(status_code=200, schema=TotalSeatsResults)
    @blueprint.arguments(GetResultsParameters, location="query")
    def get(self, parameters, districtId, scrutinyId):
        _validate_resources(districtId=districtId, scrutinyId=scrutinyId)
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.get_seats_results(
                    district_id=districtId,
                    scrutiny_id=scrutinyId,
                    limit=parameters.get("limit"),
                )
            _validate_total_seats_result(results)
            return results

        except SeatsResultsNotFoundError:
            abort(
                404,
                description=(
                    f"Seats results not found for {districtId=} and {scrutinyId=}!"
                ),
            )

    @blueprint.response(status_code=200, schema=SeatsResults)
    def post(self, districtId, scrutinyId):
        _validate_resources(districtId=districtId, scrutinyId=scrutinyId)
        try:
            with get_db_session() as session:
                repo = DhondtRepository(session)
                dhondt_service = DhondtService(repo)
                results = dhondt_service.calculate_seats(
                    district_id=districtId, scrutiny_id=scrutinyId
                )
            _validate_seats_result(results)
            return results

        except ScrutinyNotFoundError:
            abort(
                404,
                description=(
                    f"Scrutiny with scrutiny {districtId=} and {scrutinyId} not found!"
                ),
            )
