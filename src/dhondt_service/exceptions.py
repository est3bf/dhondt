from dhondt.db.exceptions import PoliticalPartyListsAlreadyExist


class DistrictsNotFoundError(Exception):
    pass


class PoliticalPartyListsNotFoundError(Exception):
    pass


class ScrutinyNotFoundError(Exception):
    pass


class SeatsResultsNotFoundError(Exception):
    pass
