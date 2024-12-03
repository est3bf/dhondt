import logging

from dhondt.db.dhondt_repository import DhondtRepository
from dhondt.dhondt_service.exceptions import (
    DistrictsNotFoundError,
    PoliticalPartyListsNotFoundError,
    ScrutinyNotFoundError,
)

logger = logging.getLogger(__name__)


def dhondt_calculation(political_parties, seats):
    logger.debug("Dhondt calculations for %s seats", seats)
    logger.debug("Political Parties list: %s", political_parties)

    # Use a new auxiliary struct for the iteration
    pplits_seats = {x["id"]: [0, x["votes"], x["name"]] for x in political_parties}

    # Iteration over total seats available
    for i in range(seats):
        # Get pplist id of the seat winner for this iteration
        idm = max((val[1] / (val[0] + 1), ippl) for ippl, val in pplits_seats.items())[
            1
        ]
        # Increment number of seat of pplist winner
        pplits_seats[idm][0] += 1
        logger.debug(
            "Iteration %s, idppl winner %s, new seats %s", i, idm, pplits_seats[idm][0]
        )
        logger.debug("Iteration %s, struct %s", i, pplits_seats)

    # generates result as expected
    result = [
        {"pplistId": ippl, "pplistName": val[2], "seats": val[0]}
        for ippl, val in pplits_seats.items()
    ]
    logger.debug("Dhondt calculations result %s", result)
    return result


class DhondtService:
    def __init__(self, repository: DhondtRepository):
        self.repository = repository

    def get_districts(self, scrutiny_date=None, district_id=None):
        districts = self.repository.get_districts(scrutiny_date, district_id)
        if districts is None:
            raise DistrictsNotFoundError(
                f"Districts with {scrutiny_date=} and {district_id=} not found!"
            )
        if district_id:
            return districts[0]
        return {"districts": districts}

    def get_political_party_lists(self, district_id, pplist_id=None):
        political_party_lists = self.repository.get_political_party_lists(
            district_id=district_id,
            pplist_id=pplist_id,
        )
        if political_party_lists is None:
            raise PoliticalPartyListsNotFoundError(
                f"Political Party Lists with {district_id=} and {pplist_id=} not found!"
            )
        if pplist_id:
            return political_party_lists[0]
        return {"politicalPartyLists": political_party_lists}

    def create_political_party_list(self, name, electors, districtId):
        result = self.repository.create_political_party_list(
            district_id=districtId,
            name=name,
            electors=electors,
        )
        if not result:
            raise PoliticalPartyListsNotFoundError(
                f"Political Party Lists with {districtId=} not found!"
            )
        return result

    def update_political_party_list(self, pplist_id, district_id, name, electors):
        political_party_lists = self.repository.get_political_party_lists(
            district_id=district_id,
            pplist_id=pplist_id,
        )
        if not political_party_lists or len(political_party_lists) > 1:
            raise PoliticalPartyListsNotFoundError(
                f"Political Party Lists with {district_id=} and {pplist_id=} not found!"
            )
        result = self.repository.update_political_party_list(
            political_party_lists[0]["id"],
            name=name,
            electors=electors,
        )
        return result

    def get_scrutinies(self, district_id, scrutiny_id=None, scrutiny_date=None):
        scrutinies = self.repository.get_scrutinies(
            district_id=district_id,
            scrutiny_date=scrutiny_date,
            scrutiny_id=scrutiny_id,
        )
        if scrutinies is None:
            raise ScrutinyNotFoundError(
                f"Scrutiny with {scrutiny_date=} and {scrutiny_id=} not found!"
            )
        if scrutiny_id:
            return scrutinies[0]
        return {"scrutinies": scrutinies}
