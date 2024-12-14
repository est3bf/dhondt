import logging

import pytest

from dhondt.dhondt_service.dhondt_service import dhondt_calculation

logger = logging.getLogger(__name__)


PPLIST_TABLE_1 = [
    {"id": 1, "districtId": 1, "name": "partido A", "votes": 340000, "electors": 22},
    {"id": 2, "districtId": 1, "name": "partido B", "votes": 280000, "electors": 22},
    {"id": 3, "districtId": 1, "name": "partido C", "votes": 160000, "electors": 13},
    {"id": 4, "districtId": 1, "name": "partido D", "votes": 60000, "electors": 50},
    {"id": 5, "districtId": 1, "name": "partido E", "votes": 15000, "electors": 50},
]

TABLE_1_RESULT_OK = [
    {"pplistId": 1, "pplistName": "partido A", "seats": 3},
    {"pplistId": 2, "pplistName": "partido B", "seats": 3},
    {"pplistId": 3, "pplistName": "partido C", "seats": 1},
    {"pplistId": 4, "pplistName": "partido D", "seats": 0},
    {"pplistId": 5, "pplistName": "partido E", "seats": 0},
]

TABLE_1_RESULT_0 = [
    {k: v if k != "seats" else 0 for k, v in s.items()} for s in TABLE_1_RESULT_OK
]
TABLE_1_RESULT_MALFORMED_1 = [
    {k: v if k != "votes" else None for k, v in s.items()} for s in PPLIST_TABLE_1
]

TABLE_1_RESULT_MALFORMED_2 = [
    {k: v for k, v in s.items() if k != "votes"} for s in PPLIST_TABLE_1
]

TABLE_1_RESULT_MALFORMED_3 = [
    {k: v for k, v in s.items() if k != "id"} for s in PPLIST_TABLE_1
]

TABLE_1_RESULT_MALFORMED_4 = [
    {k: v for k, v in s.items() if k != "name"} for s in PPLIST_TABLE_1
]

TABLE_1_RESULT_MALFORMED_5 = [
    {k: v for k, v in s.items() if k != "districtId"} for s in PPLIST_TABLE_1
]

TABLE_1_RESULT_MALFORMED_6 = [
    {k: v for k, v in s.items() if k != "electors"} for s in PPLIST_TABLE_1
]

PPLIST_TABLE_2 = [
    {"id": 10, "districtId": 1, "name": "partido A", "votes": 73000, "electors": 22},
    {"id": 20, "districtId": 1, "name": "partido B", "votes": 27000, "electors": 22},
    {"id": 30, "districtId": 1, "name": "partido C", "votes": 311000, "electors": 13},
    {"id": 40, "districtId": 1, "name": "partido D", "votes": 2000, "electors": 50},
    {"id": 51, "districtId": 1, "name": "partido E", "votes": 184000, "electors": 50},
    {"id": 52, "districtId": 1, "name": "partido F", "votes": 391000, "electors": 50},
    {"id": 53, "districtId": 1, "name": "partido G", "votes": 12000, "electors": 50},
]

TABLE_2_RESULT_OK = [
    {"pplistId": 10, "pplistName": "partido A", "seats": 1},
    {"pplistId": 20, "pplistName": "partido B", "seats": 0},
    {"pplistId": 30, "pplistName": "partido C", "seats": 7},
    {"pplistId": 40, "pplistName": "partido D", "seats": 0},
    {"pplistId": 51, "pplistName": "partido E", "seats": 4},
    {"pplistId": 52, "pplistName": "partido F", "seats": 9},
    {"pplistId": 53, "pplistName": "partido G", "seats": 0},
]

TABLE_2_RESULT_0 = [
    {k: v if k != "seats" else 0 for k, v in s.items()} for s in TABLE_2_RESULT_OK
]

doundt_calc_data_ok = [
    (PPLIST_TABLE_1, 7, TABLE_1_RESULT_OK),
    (TABLE_1_RESULT_MALFORMED_5, 7, TABLE_1_RESULT_OK),
    (TABLE_1_RESULT_MALFORMED_6, 7, TABLE_1_RESULT_OK),
    (PPLIST_TABLE_2, 21, TABLE_2_RESULT_OK),
]


doundt_calc_data_err = [
    (PPLIST_TABLE_1, 0, TABLE_1_RESULT_0),
    (PPLIST_TABLE_2, -1, TABLE_2_RESULT_0),
]


doundt_calc_data_malformed = [
    (TABLE_1_RESULT_MALFORMED_2, "votes"),
    (TABLE_1_RESULT_MALFORMED_3, "id"),
    (TABLE_1_RESULT_MALFORMED_4, "name"),
]


class TestService:

    @pytest.mark.parametrize("pplists, seats, result_ok", doundt_calc_data_ok)
    def test_dhondt_calculation_ok(self, pplists, seats, result_ok):
        result = dhondt_calculation(political_parties=pplists, seats=seats)
        assert result_ok == result

    @pytest.mark.parametrize("pplists, seats, result_err", doundt_calc_data_err)
    def test_dhondt_calculation_error(self, pplists, seats, result_err):
        result = dhondt_calculation(political_parties=pplists, seats=seats)
        assert result_err == result

    def test_dhondt_calculation_error_type(self):
        with pytest.raises(TypeError) as excinfo:
            dhondt_calculation(political_parties=TABLE_1_RESULT_MALFORMED_1, seats=10)
        assert "unsupported operand" in str(excinfo.value) and "NoneType" in str(
            excinfo.value
        )
        with pytest.raises(TypeError) as excinfo:
            dhondt_calculation(political_parties=PPLIST_TABLE_2, seats=1.5)
        assert "float' object cannot be interpreted as an integer" in str(excinfo.value)

    @pytest.mark.parametrize("pplists, key", doundt_calc_data_malformed)
    def test_dhondt_calculation_malformed(self, pplists, key):
        with pytest.raises(KeyError) as excinfo:
            dhondt_calculation(political_parties=pplists, seats=10)
        assert key in str(excinfo.value)
