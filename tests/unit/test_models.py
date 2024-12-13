import pytest
from copy import deepcopy
import string
from hypothesis import strategies as st
from hypothesis import given, Verbosity, settings, HealthCheck

from sqlalchemy.exc import IntegrityError

from dhondt.db.controller import DB
from dhondt.db.tabledefs import (
    ScrutinyTable,
    DistrictTable,
    PoliticalPartyListTable,
    SeatsPoliticalPartiesTable,
    DhondtResultTable,
)


value_strategy_int_db = st.integers(min_value=pow(-2, 63), max_value=(pow(2, 63) - 1))
value_strategy_positive_db = st.integers(min_value=0, max_value=(pow(2, 63) - 1))
value_strategy_str_db = st.text(
    min_size=1, max_size=200, alphabet=string.ascii_letters + string.digits
)
value_strategy_name = value_strategy_str_db

scrutiny_strategy = st.fixed_dictionaries(
    {
        "district_id": st.just(1),  # Fixed to 1
        "voting_date": st.dates(),
        "scrutiny_date": st.dates(),
        "seats": value_strategy_positive_db,
        "name": value_strategy_name,
    }
)

district_strategy = st.fixed_dictionaries(
    {
        "name": value_strategy_name,
    }
)

pplist_strategy = st.fixed_dictionaries(
    {
        "district_id": st.just(1),  # Fixed to 1
        "name": value_strategy_name,
        "votes": value_strategy_positive_db,
        "electors": value_strategy_positive_db,
    }
)

seats_ppl_strategy = st.fixed_dictionaries(
    {
        "politicalpartylist_id": st.just(1),  # Fixed to 1,
        "dhondtresult_id": value_strategy_positive_db,
        "seats": value_strategy_positive_db,
    }
)

dhondtresult_strategy = st.fixed_dictionaries(
    {
        "result_date": st.dates(),
    }
)


class TestModels:

    def setup_class(cls):
        DB.init_memory_db()
        cls.result_cnt = 1

    def tear_down_class():
        DB.drop_db_memory()

    def _add_reg(self, db_session, table, values):
        record = table(**values)
        db_session.add(record)
        db_session.commit()
        return record

    def _check_add_reg(self, db_session, table, values, resp_ok):
        record = self._add_reg(db_session=db_session, table=table, values=values)
        res = record.dict()
        if "id" in res.keys():
            id = res.pop("id")
            assert isinstance(id, int)
        else:
            id = record.id
        assert res == resp_ok
        records = db_session.query(table).filter(id == table.id).all()
        assert len(records) == 1
        res = records[0].dict()
        if "id" in res.keys():
            assert res.pop("id") == id
        assert res == resp_ok

    def _integrity_check(self, db_session, table, value):
        for var in value.keys():
            col = table.__table__.columns[var]
            if col.nullable == True or not col.default:
                # remove column to test nulleable condition
                err = deepcopy(value)
                err.pop(var)
                with pytest.raises(IntegrityError) as excinfo:
                    record = table(**err)
                    db_session.add(record)
                    db_session.commit()
            elif col.unique == True:
                # test two times for unique condition
                with pytest.raises(IntegrityError) as excinfo:
                    record = table(**value)
                    db_session.add(record)
                    db_session.add(record)
                    db_session.commit()
            else:
                continue
            db_session.rollback()
            assert f"constraint failed: {table.__tablename__}.{var}" in str(
                excinfo.value
            ) or f"UNIQUE constraint failed: {table.__tablename__}" in str(
                excinfo.value
            )

    ##############################
    # DistrictTable
    ##############################
    @settings(
        verbosity=Verbosity.verbose,
        max_examples=20,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    @given(district=district_strategy)
    def test_districttable_ok(self, db_session, district):
        resp_ok = {
            "name": district["name"].lower(),
        }
        self._check_add_reg(
            table=DistrictTable, db_session=db_session, values=district, resp_ok=resp_ok
        )

    @settings(
        verbosity=Verbosity.verbose,
        max_examples=1,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    @given(district=district_strategy)
    def test_districttable_fails(self, db_session, district):
        self._integrity_check(
            db_session=db_session, table=DistrictTable, value=district
        )

    ##############################
    # ScrutinyTable
    ##############################
    @settings(
        verbosity=Verbosity.verbose,
        max_examples=20,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    @given(scrutiny=scrutiny_strategy)
    def test_scrutinytable_ok(self, db_session, scrutiny):
        resp_ok = {
            "districtId": scrutiny["district_id"],
            "votingDate": scrutiny["voting_date"].isoformat(),
            "scrutinyDate": scrutiny["scrutiny_date"].isoformat(),
            "seats": scrutiny["seats"],
            "name": scrutiny["name"],
        }
        self._check_add_reg(
            table=ScrutinyTable, db_session=db_session, values=scrutiny, resp_ok=resp_ok
        )

    @settings(
        verbosity=Verbosity.verbose,
        max_examples=1,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    @given(scrutiny=scrutiny_strategy)
    def test_scrityny_fails(self, db_session, scrutiny):
        self._integrity_check(
            db_session=db_session, table=ScrutinyTable, value=scrutiny
        )

    ##############################
    # PoliticalPartyListTable
    ##############################
    @settings(
        verbosity=Verbosity.verbose,
        max_examples=20,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    @given(pplist=pplist_strategy)
    def test_pplisttable_ok(self, db_session, pplist):
        resp_ok = {
            "districtId": pplist["district_id"],
            "name": pplist["name"].lower(),
            "votes": pplist["votes"],
            "electors": pplist["electors"],
        }
        self._check_add_reg(
            table=PoliticalPartyListTable,
            db_session=db_session,
            values=pplist,
            resp_ok=resp_ok,
        )
        # to remove duplicates
        db_session.query(PoliticalPartyListTable).delete()
        db_session.commit()

    @settings(
        verbosity=Verbosity.verbose,
        max_examples=1,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    @given(pplist=pplist_strategy)
    def test_pplisttable_fails(self, db_session, pplist):
        self._integrity_check(
            db_session=db_session, table=PoliticalPartyListTable, value=pplist
        )

    ##############################
    # SeatsPoliticalPartiesTable
    ##############################
    @settings(
        verbosity=Verbosity.verbose,
        max_examples=20,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    @given(seats_ppl=seats_ppl_strategy, pplist=pplist_strategy)
    def test_seatsppltable_ok(self, db_session, seats_ppl, pplist):
        # Needs at least one ppl
        self._add_reg(
            db_session=db_session, table=PoliticalPartyListTable, values=pplist
        )
        resp_ok = {
            "pplistId": seats_ppl["politicalpartylist_id"],
            "seats": seats_ppl["seats"],
            "pplistName": pplist["name"].lower(),
        }
        self._check_add_reg(
            table=SeatsPoliticalPartiesTable,
            db_session=db_session,
            values=seats_ppl,
            resp_ok=resp_ok,
        )
        # to remove duplicates
        db_session.query(PoliticalPartyListTable).delete()
        db_session.query(SeatsPoliticalPartiesTable).delete()
        db_session.commit()

    @settings(
        verbosity=Verbosity.verbose,
        max_examples=1,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    @given(seats_ppl=seats_ppl_strategy)
    def test_seatsppltable_fails(self, db_session, seats_ppl):
        self._integrity_check(
            db_session=db_session, table=SeatsPoliticalPartiesTable, value=seats_ppl
        )

    ##############################
    # DhondtResultTable
    ##############################
    @settings(
        verbosity=Verbosity.verbose,
        max_examples=20,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    @given(
        scrutiny=scrutiny_strategy,
        pplist=pplist_strategy,
        dhondtresult=dhondtresult_strategy,
    )
    def test_dhondtresult_ok(self, db_session, scrutiny, pplist, dhondtresult):
        # Needs at least one ppl
        scrutiny_record = self._add_reg(
            db_session=db_session, table=ScrutinyTable, values=scrutiny
        )
        self._add_reg(
            db_session=db_session, table=PoliticalPartyListTable, values=pplist
        )
        seats_ppl = {
            "politicalpartylist_id": 1,
            "dhondtresult_id": self.result_cnt,
            "seats": 20,
        }
        self._add_reg(
            db_session=db_session, table=SeatsPoliticalPartiesTable, values=seats_ppl
        )
        resp_ok = {
            "resultId": self.result_cnt,
            "districtId": 1,
            "scrutinyId": scrutiny_record.id,
            "scrutinyName": scrutiny_record.name,
            "calculationDate": dhondtresult["result_date"].isoformat(),
            "seatsResults": [
                {
                    "pplistId": seats_ppl["politicalpartylist_id"],
                    "seats": seats_ppl["seats"],
                    "pplistName": pplist["name"].lower(),
                }
            ],
        }
        dhondtresult["scrutiny_id"] = scrutiny_record.id
        self.result_cnt += 1
        self._check_add_reg(
            table=DhondtResultTable,
            db_session=db_session,
            values=dhondtresult,
            resp_ok=resp_ok,
        )
        # to remove duplicates
        db_session.query(PoliticalPartyListTable).delete()
        db_session.query(SeatsPoliticalPartiesTable).delete()
        db_session.commit()

    @settings(
        verbosity=Verbosity.verbose,
        max_examples=1,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    @given(
        dhondtresult=dhondtresult_strategy,
    )
    def test_dhondtresult_fails(self, db_session, dhondtresult):
        dhondtresult["scrutiny_id"] = 1
        self._integrity_check(
            db_session=db_session, table=DhondtResultTable, value=dhondtresult
        )
