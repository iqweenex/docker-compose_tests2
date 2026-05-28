import pytest
from tests.helpers.api_client import ApiClient


class TestApiClient:
    @pytest.fixture
    def client(self):
        return ApiClient(base_url="http://127.0.0.1:8001")

    def test_build_url_simple_path(self, client):
        url = client._build_url("/students/")
        assert url == "http://127.0.0.1:8001/students/"

    def test_build_url_no_slash(self, client):
        url = client._build_url("students/")
        assert url == "http://127.0.0.1:8001/students/"

    def test_build_url_nested_path(self, client):
        url = client._build_url("/grades/stats/")
        assert url == "http://127.0.0.1:8001/grades/stats/"

    def test_base_url_trailing_slash_removed(self):
        client = ApiClient(base_url="http://127.0.0.1:8001/")
        url = client._build_url("/students/")
        assert url == "http://127.0.0.1:8001/students/"

    def test_get_request_without_auth_returns_401_or_403(self, client):
        response = client.get("/grades/stats/")
        assert response.status_code in [401, 403]
