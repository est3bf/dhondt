import os
import logging

from sqlalchemy.exc import (
    NoReferencedColumnError,
)
from dhondt.db.controller import DB
from dhondt.db.tabledefs import (
    ScrutinyTable,
    DistrictTable,
    PoliticalPartyListTable,
)

logger = logging.getLogger(__name__)

DB_URL = os.getenv("DB_URL", "127.0.0.1") + ":" + os.getenv("DB_PORT", "5432")
DB_DATABASE = os.getenv("DB_NAME", "dhondt")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSW = os.getenv("DB_PASS", "postgres")

DB.init(DB_URL, DB_DATABASE, DB_USER, DB_PASSW)


class DhondtRepository:
    def __init__(self, db_session):
        self.session = db_session

    def get_districts(self, scrutiny_date, district_id):
        query = self.session.query(DistrictTable)
        if district_id:
            logger.info("get_districts with district_id: %s", district_id)
            query = query.filter(district_id == DistrictTable.id)
        if scrutiny_date:
            logger.info("get_districts with scrutiny_date: %s", scrutiny_date)
            query = query.join(
                ScrutinyTable, ScrutinyTable.district_id == DistrictTable.id
            ).filter(scrutiny_date == ScrutinyTable.scrutiny_date)

        records = query.all()
        logger.info("records: %s", records)
        results = None
        if records:
            results = [record.dict() for record in records]
        logger.info("values: %s", results)
        return results

    def get_political_party_lists(self, district_id, pplist_id=None):
        query = (
            self.session.query(PoliticalPartyListTable)
            .join(
                DistrictTable, DistrictTable.id == PoliticalPartyListTable.district_id
            )
            .filter(district_id == DistrictTable.id)
        )
        if pplist_id:
            logger.info("get_political_party_lists with pplist_id: %s", pplist_id)
            query = query.filter(pplist_id == PoliticalPartyListTable.id)
        records = query.all()
        logger.info("records: %s", records)
        results = None
        if records:
            results = [record.dict() for record in records]
        logger.info("values: %s", results)
        return results

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

    def update_political_party_list(self, pplist_id, **kwargs):
        record = (
            self.session.query(PoliticalPartyListTable)
            .filter(pplist_id == PoliticalPartyListTable.id)
            .first()
        )
        for argn, argv in kwargs.items():
            setattr(record, argn, argv)
        self.session.commit()
        return record.dict()
