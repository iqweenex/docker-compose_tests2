import pytest
import requests.status_codes
from faker import Faker

from services.university.helpers.group_helper import GroupHelper

faker = Faker()


@pytest.mark.xfail
class TestGroupContract:
    def test_create_group_anonym(self, university_api_utils_anonym):
        group_helper = GroupHelper(api_utils=university_api_utils_anonym)
        response = group_helper.post_group({"name": faker.name()})

        assert response.status_code == requests.status_codes.codes.unauthorized, \
            f"Wrong status code. \n" \
            f"Actual: {response.status_code}\n" \
            f"Expected: {requests.status_codes.codes.unauthorized}"
