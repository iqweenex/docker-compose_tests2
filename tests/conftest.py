import pytest
from tests.utils.logger import Logger
from tests.helpers.api_client import ApiClient
from tests.helpers.auth_manager import AuthManager
from tests.helpers.data_generator import DataGenerator
from requests.exceptions import HTTPError
from tests.services.university_service import UniversityService

AUTH_URL = "http://127.0.0.1:8000"
UNIVERSITY_URL = "http://127.0.0.1:8001"


@pytest.fixture(scope="session")
def auth_api_client():
    return ApiClient(AUTH_URL)


@pytest.fixture(scope="session")
def credentials():
    gen = DataGenerator()
    return gen.unique_credentials()


@pytest.fixture(scope="session")
def auth_manager(auth_api_client, credentials):
    manager = AuthManager(auth_api_client)
    try:
        Logger.info(f"Логин: {credentials['username']}")
        manager.login(credentials["username"], credentials["password"])
    except HTTPError as e:
        if e.response.status_code == 401:
            Logger.info(f"Регистрация: {credentials['username']}")
            manager.register(
                credentials["username"],
                credentials["password"],
                email=f"{credentials['username']}@test.com"
            )
            Logger.info(f"Повторный логин: {credentials['username']}")
            manager.login(credentials["username"], credentials["password"])
        else:
            Logger.error(f"Ошибка авторизации: {e.response.status_code}")
            raise
    return manager


@pytest.fixture(scope="session")
def api_client():
    return ApiClient(UNIVERSITY_URL)


@pytest.fixture(scope="session")
def university_service(api_client, auth_manager):
    return UniversityService(api_client, auth_manager)


@pytest.fixture(scope="function")
def generator():
    return DataGenerator()
