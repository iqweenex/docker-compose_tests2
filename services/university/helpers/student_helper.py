import requests

from services.general.helpers.base_helper import BaseHelper


class StudentHelper(BaseHelper):
    ENDPOINT_PREFIX = "/students"
    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"

    def post_student(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def put_student(self, student_id: int, json: dict) -> requests.Response:
        response = self.api_utils.put(f"{self.ROOT_ENDPOINT}{student_id}/", json=json)
        return response

