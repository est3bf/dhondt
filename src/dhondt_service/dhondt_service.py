import logging

from dhondt.db.dhondt_repository import DhondtRepository
from dhondt.dhondt_service.exceptions import (
    DistrictsNotFoundError,
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
