import os
import logging
from datetime import datetime

from sqlalchemy.exc import (
    NoReferencedColumnError,
    IntegrityError,
)
from psycopg2.errors import UniqueViolation, ForeignKeyViolation

from dhondt.db.controller import DB
from dhondt.db.tabledefs import (
    ScrutinyTable,
    DistrictTable,
    PoliticalPartyListTable,
    SeatsPoliticalPartiesTable,
    DhondtResultTable,
)
from dhondt.db.exceptions import PoliticalPartyListsAlreadyExist

logger = logging.getLogger(__name__)

DB_URL = os.getenv("DB_URL", "127.0.0.1") + ":" + os.getenv("DB_PORT", "5432")
DB_DATABASE = os.getenv("DB_NAME", "dhondt")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSW = os.getenv("DB_PASS", "postgres")


def init_repository(use_memory_db):
    """Init the repository database

    This function is used to instance the Database class Singleton in the controller module.
    The goal of this function is to control the persistent or memory database type. Memory database is intended to be used only in unit testing.

    :param use_memory_db: If not None type, the memory database is used.
    """
    DB.init(DB_URL, DB_DATABASE, DB_USER, DB_PASSW, memory=use_memory_db)


class DhondtRepository:
    """
    This class is used to decouple the business layer from r from the implementation
    details of the database or repository.

    This follow the repository pattern.

    The SqlAlchemy ORM library controls the database and it's setting up by the *tabledefs* module and controller by the *controller* module.

    The class interacts with the repository controller through database session to perform actions, which is provided by the constructor class call.
    """

    def __init__(self, db_session):
        self.session = db_session

    def get_districts(self, scrutiny_date, district_id):
        try:
            query = self.session.query(DistrictTable)
            if district_id:
                logger.debug("get_districts with district_id: %s", district_id)
                query = query.filter(district_id == DistrictTable.id)
            if scrutiny_date:
                logger.debug("get_districts with scrutiny_date: %s", scrutiny_date)
                query = query.join(
                    ScrutinyTable, ScrutinyTable.district_id == DistrictTable.id
                ).filter(scrutiny_date == ScrutinyTable.scrutiny_date)

            records = query.all()
            logger.debug("records: %s", records)
            results = None
            if records:
                results = [record.dict() for record in records]
            logger.debug("values: %s", results)
            return results
        except IntegrityError as e:
            logger.debug("get_districts IntegrityError: %s", e)
            return None

    def get_political_party_lists(self, district_id, pplist_id=None):
        try:
            query = (
                self.session.query(PoliticalPartyListTable)
                .join(
                    DistrictTable,
                    DistrictTable.id == PoliticalPartyListTable.district_id,
                )
                .filter(district_id == DistrictTable.id)
            )
            if pplist_id:
                logger.debug("get_political_party_lists with pplist_id: %s", pplist_id)
                query = query.filter(pplist_id == PoliticalPartyListTable.id)
            records = query.all()
            logger.debug("records: %s", records)
            results = None
            if records:
                results = [record.dict() for record in records]
            logger.debug("values: %s", results)
            return results
        except IntegrityError as e:
            logger.debug("get_political_party_lists IntegrityError: %s", e)
            return None

    def create_political_party_list(self, name, electors, district_id):
        try:
            record = PoliticalPartyListTable(
                district_id=district_id,
                name=name,
                electors=electors,
            )
            self.session.add(record)
            self.session.commit()
            return record.dict()
        except NoReferencedColumnError:
            return None
        except IntegrityError as e:
            logger.debug("create_political_party_list error: %s", e)
            if isinstance(e.orig, UniqueViolation):
                raise PoliticalPartyListsAlreadyExist(
                    f"Political Party Lists with {name=} already exits!"
                )
            return None

    def update_political_party_list(self, pplist_id, **kwargs):
        try:
            record = (
                self.session.query(PoliticalPartyListTable)
                .filter(pplist_id == PoliticalPartyListTable.id)
                .first()
            )
            for argn, argv in kwargs.items():
                setattr(record, argn, argv)
            self.session.commit()
            return record.dict()
        except IntegrityError as e:
            logger.debug("update_political_party_list error: %s", e)
            if isinstance(e.orig, UniqueViolation):
                raise PoliticalPartyListsAlreadyExist(
                    f"Political Party Lists with {kwargs['name']=} already exits!"
                )
            return None

    def get_scrutinies(self, district_id, scrutiny_id=None, scrutiny_date=None):
        try:
            query = (
                self.session.query(ScrutinyTable)
                .join(DistrictTable, DistrictTable.id == ScrutinyTable.district_id)
                .filter(district_id == DistrictTable.id)
            )
            if scrutiny_id is not None:
                logger.debug("get_scrutinies with scrutiny_id: %s", scrutiny_id)
                query = query.filter(scrutiny_id == ScrutinyTable.id)
            if scrutiny_date:
                logger.debug("get_scrutinies with scrutiny_date: %s", scrutiny_date)
                query = query.filter(scrutiny_date == ScrutinyTable.scrutiny_date)
            records = query.all()
            logger.debug("records: %s", records)
            results = None
            if records:
                results = [record.dict() for record in records]
            logger.debug("values: %s", results)
            return results
        except IntegrityError as e:
            logger.debug("get_scrutinies IntegrityError: %s", e)
            return None

    def create_scrutiny(self, district_id, name, voting_date, scrutiny_date, seats):
        try:
            record = ScrutinyTable(
                district_id=district_id,
                voting_date=voting_date,
                scrutiny_date=scrutiny_date,
                seats=seats,
                name=name,
            )
            self.session.add(record)
            self.session.commit()
            return record.dict()
        except IntegrityError as e:
            logger.debug("create_scrutiny IntegrityError: %s", e)
            if isinstance(e.orig, ForeignKeyViolation):
                return None
            raise IntegrityError(e)
        except NoReferencedColumnError:
            return None

    def create_dhondt_result(self, scrutiny_id, seats_result):
        try:
            record = DhondtResultTable(
                scrutiny_id=scrutiny_id, result_date=datetime.now()
            )
            for res in seats_result:
                record.seatspoliticalparties.append(
                    SeatsPoliticalPartiesTable(
                        politicalpartylist_id=res["pplistId"], seats=res["seats"]
                    )
                )
            self.session.add(record)
            self.session.commit()
            return record.dict()
        except IntegrityError as e:
            logger.debug("create_scrutiny IntegrityError: %s", e)
            if isinstance(e.orig, ForeignKeyViolation):
                return None
            raise IntegrityError(e)

    def get_seats_results(self, district_id, scrutiny_id, limit=None):
        try:
            logger.debug(
                "get_seats_results with district_id %d and scrutiny_id: %s",
                district_id,
                scrutiny_id,
            )
            records = (
                self.session.query(DhondtResultTable)
                .filter(DhondtResultTable.scrutiny_id == scrutiny_id)
                .limit(limit)
                .all()
            )
            result = None
            if records:
                result = [res.dict() for res in records]
            logger.debug("result: %s", result)
            return result
        except IntegrityError as e:
            logger.debug("get_seats_results IntegrityError: %s", e)
            return None
