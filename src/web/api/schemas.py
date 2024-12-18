import string
from marshmallow import Schema, fields, validate, EXCLUDE

NAME_FIELD_REQ = fields.String(
    validate=validate.ContainsOnly(
        string.ascii_letters + string.digits + string.punctuation + string.whitespace
    ),
    required=True,
)

INTEGER_INT32_POS_REQ_1 = fields.Integer(
    validate=validate.Range(min=1, min_inclusive=True, max=2**31),
    required=True,
)

INTEGER_INT32_POS_REQ_0 = fields.Integer(
    validate=validate.Range(min=0, min_inclusive=True, max=2**31),
    required=True,
)

INTEGER_ID = INTEGER_INT32_POS_REQ_1


class CreatePoliticalPartyList(Schema):
    class Meta:
        unknown = EXCLUDE

    name = NAME_FIELD_REQ
    electors = INTEGER_INT32_POS_REQ_1


class PoliticalPartyList(CreatePoliticalPartyList):
    id = INTEGER_ID
    districtId = INTEGER_ID
    votes = INTEGER_INT32_POS_REQ_0


class GetPoliticalPartyLists(Schema):
    class Meta:
        unknown = EXCLUDE

    politicalPartyLists = fields.List(fields.Nested(PoliticalPartyList), required=True)


class District(Schema):
    id = INTEGER_ID
    name = NAME_FIELD_REQ


class GetDistricts(Schema):
    class Meta:
        unknown = EXCLUDE

    districts = fields.List(fields.Nested(District), required=True)


class CreateScrutiny(Schema):
    class Meta:
        unknown = EXCLUDE

    seats = INTEGER_INT32_POS_REQ_1
    name = NAME_FIELD_REQ
    votingDate = fields.Date(required=True)
    scrutinyDate = fields.Date(required=True)


class Scrutiny(CreateScrutiny):
    id = INTEGER_ID
    districtId = INTEGER_ID


class GetScrutinies(Schema):
    class Meta:
        unknown = EXCLUDE

    scrutinies = fields.List(fields.Nested(Scrutiny), required=True)


class SeatsResult(Schema):
    class Meta:
        unknown = EXCLUDE

    pplistId = INTEGER_ID
    pplistName = NAME_FIELD_REQ
    seats = INTEGER_INT32_POS_REQ_0


class SeatsResults(Schema):
    class Meta:
        unknown = EXCLUDE

    resultId = INTEGER_ID
    scrutinyId = INTEGER_ID
    scrutinyName = NAME_FIELD_REQ
    calculationDate = fields.Date(required=True)
    seatsResults = fields.List(fields.Nested(SeatsResult), required=True)


class TotalSeatsResults(Schema):
    class Meta:
        unknown = EXCLUDE

    scrutinyResults = fields.List(fields.Nested(SeatsResults), required=True)


class GetDistrictsParameters(Schema):
    class Meta:
        unknown = EXCLUDE

    scrutinyDate = fields.Date()


class GetScrutiniesParameters(Schema):
    class Meta:
        unknown = EXCLUDE

    scrutinyDate = fields.Date()


class UpgradeVoteParameters(Schema):
    class Meta:
        unknown = EXCLUDE

    votes = INTEGER_INT32_POS_REQ_0


class GetResultsParameters(Schema):
    class Meta:
        unknown = EXCLUDE

    limit = INTEGER_INT32_POS_REQ_0


class ResourceId(Schema):
    class Meta:
        unknown = EXCLUDE

    id = INTEGER_ID
