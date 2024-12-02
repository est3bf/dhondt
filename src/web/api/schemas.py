from marshmallow import Schema, fields, validate, EXCLUDE


class CreatePoliticalPartyList(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.String(required=True)
    electors = fields.Integer(
        validate=validate.Range(1, min_inclusive=True),
        required=True,
    )


class PoliticalPartyList(CreatePoliticalPartyList):
    id = fields.Integer(
        validate=validate.Range(1, min_inclusive=True),
        required=True,
    )
    districtId = fields.Integer(
        validate=validate.Range(1, min_inclusive=True),
        required=True,
    )
    votes = fields.Integer(
        validate=validate.Range(0, min_inclusive=True),
        required=True,
    )


class GetPoliticalPartyLists(Schema):
    class Meta:
        unknown = EXCLUDE

    politicalPartyLists = fields.List(fields.Nested(PoliticalPartyList), required=True)


class District(Schema):
    id = fields.Integer(
        validate=validate.Range(1, min_inclusive=True),
        required=True,
    )
    name = fields.String(required=True)


class GetDistricts(Schema):
    class Meta:
        unknown = EXCLUDE

    districts = fields.List(fields.Nested(District), required=True)


class CreateScrutiny(Schema):
    class Meta:
        unknown = EXCLUDE

    seats = fields.Integer(
        validate=validate.Range(1, min_inclusive=True),
        required=True,
    )
    name = fields.String(required=True)
    votingDate = fields.DateTime(required=True)
    scrutinyDate = fields.DateTime(required=True)


class Scrutiny(CreateScrutiny):
    id = fields.Integer(
        validate=validate.Range(1, min_inclusive=True),
        required=True,
    )
    districtId = fields.Integer(
        validate=validate.Range(1, min_inclusive=True),
        required=True,
    )


class GetScrutinies(Schema):
    class Meta:
        unknown = EXCLUDE

    scrutinies = fields.List(fields.Nested(Scrutiny), required=True)


class SeatsResult(Schema):
    class Meta:
        unknown = EXCLUDE

    pplistId = fields.Integer(
        validate=validate.Range(1, min_inclusive=True),
        required=True,
    )
    pplistName = fields.String(required=True)
    seats = fields.Integer(
        validate=validate.Range(0, min_inclusive=True),
        required=True,
    )


class SeatsResults(Schema):
    class Meta:
        unknown = EXCLUDE

    resultId = fields.Integer(
        validate=validate.Range(1, min_inclusive=True),
        required=True,
    )
    scrutinyId = fields.Integer(
        validate=validate.Range(1, min_inclusive=True),
        required=True,
    )
    scrutinyName = fields.String(required=True)
    calculationDate = fields.DateTime(required=True)
    seatsResults = fields.List(fields.Nested(SeatsResult), required=True)


class TotalSeatsResults(Schema):
    class Meta:
        unknown = EXCLUDE

    scrutinyResults = fields.List(fields.Nested(SeatsResults), required=True)


class GetDistrictsParameters(Schema):
    class Meta:
        unknown = EXCLUDE

    scrutinyDate = fields.DateTime()


class GetScrutiniesParameters(Schema):
    class Meta:
        unknown = EXCLUDE

    scrutinyDate = fields.DateTime()


class UpgradeVoteParameters(Schema):
    class Meta:
        unknown = EXCLUDE

    votes = fields.Integer(
        validate=validate.Range(0, min_inclusive=True),
        required=True,
    )


class GetResultsParameters(Schema):
    class Meta:
        unknown = EXCLUDE

    limit = fields.Integer(
        validate=validate.Range(0, min_inclusive=True),
        required=False,
    )
