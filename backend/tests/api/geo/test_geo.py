import http

import pytest

from tests import api_requests
from tests.api.geo import expected


class TestGeoApi:

    def test_get_countries_list_success(self, anonym_client):
        resp = api_requests.get_countries(anonym_client)
        assert resp.status_code == http.HTTPStatus.OK

    def test_get_cities_for_county(self, anonym_client, country_usa):
        resp = api_requests.get_cities(
            anonym_client, {'state_county_id': country_usa.id}
        )
        assert resp.status_code == http.HTTPStatus.OK

    def test_filter_cities_by_name(self, anonym_client):
        new_york_name = 'New York'
        resp = api_requests.get_cities(
            anonym_client, {'name': new_york_name}
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()['results'])
        for city in resp.json()['results']:
            assert new_york_name in city['name']

    @pytest.mark.parametrize(('query_params', 'exp'), (
        (
            {'search': 'new york'},
            expected.EXPECTED_NEW_YORK
        ),
        (
            {'search': '10001'},
            expected.EXPECTED_10001
        ),
        (
            {'search': 'alabA'},
            expected.EXPECTED_ALABA
        ),
    ))
    def test_locations_autocomplete_for_search(
            self, anonym_client, query_params, exp):
        resp = api_requests.get_locations(
            anonym_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json() == exp

    @pytest.mark.parametrize(('query_params', 'exp'), (
        (
            {'name': 'Michigan'},
            expected.EXPECTED_MICHIGAN_TIMEZONE
        ),
        (
            {'name': 'New yo'},
            expected.EXPECTED_NEW_YORK_TIMEZONE
        ),
    ))
    def test_get_timezone_search(self, anonym_client, query_params, exp):
        resp = api_requests.get_timezones(
            anonym_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json() == exp
