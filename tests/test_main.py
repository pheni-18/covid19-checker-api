from fastapi.testclient import TestClient

import datetime
import main
import pytest


class TestStr8ToDate:
    def test_success(self):
        assert main.str8_to_date('20210101') == datetime.date(2021, 1, 1)

    def test_longer(self):
        with pytest.raises(main.ValidationError):
            main.str8_to_date('202101011')

    def test_shorter(self):
        with pytest.raises(main.ValidationError):
            main.str8_to_date('2021010')

    def test_include_alphabet(self):
        with pytest.raises(main.ValidationError):
            main.str8_to_date('2021010a')


class TestGetAll:
    @pytest.fixture
    def client(self):
        return TestClient(main.app)

    @pytest.fixture
    def all_data(self):
        return [
            {'name': 'name1', 'date': datetime.date(2021, 1, 1), 'count': 1},
            {'name': 'name2', 'date': datetime.date(2021, 1, 1), 'count': 2},
            {'name': 'name3', 'date': datetime.date(2021, 1, 1), 'count': 3},
        ]

    def test_success(self, mocker, client, all_data):
        mocker.patch('services.CovidService.get_all_by_date', return_value=all_data)
        res = client.get('/all?date=20210101')
        assert res.status_code == 200
        assert res.json() == [
            {'name': 'name1', 'date': '2021-01-01', 'count': 1},
            {'name': 'name2', 'date': '2021-01-01', 'count': 2},
            {'name': 'name3', 'date': '2021-01-01', 'count': 3},
        ]

    def test_bad_request(self, mocker, client):
        mocker.patch('services.CovidService.get_all_by_date', return_value=[])
        res = client.get('/all?date=20210101a')
        assert res.status_code == 400
        assert res.json() == {'detail': "'date' is invalid"}

    def test_(self, mocker, client):
        mocker.patch('services.CovidService.get_all_by_date', side_effect=Exception)
        res = client.get('/all?date=20210101')
        assert res.status_code == 500
        assert res.json() == {'detail': 'Open data API error'}
