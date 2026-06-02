import requests

from services.general.helpers.base_helper import BaseHelper


class GradeHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grades"
    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"

    def post_grade(self, data: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, data=data)
        return response

    def put_grade(self, grade_id: int, data: dict) -> requests.Response:
        response = self.api_utils.put(f"{self.ROOT_ENDPOINT}{grade_id}/", data=data)
        return response

    def delete_grade(self, grade_id: int) -> requests.Response:
        response = self.api_utils.delete(f"{self.ROOT_ENDPOINT}{grade_id}/")
        return response

    def get_grades_stats(self, student_id: int = None, teacher_id: int = None,
                         group_id: int = None) -> requests.Response:
        params = {}
        if student_id is not None:
            params['student_id'] = student_id
        if teacher_id is not None:
            params['teacher_id'] = teacher_id
        if group_id is not None:
            params['group_id'] = group_id

        response = self.api_utils.get(f"{self.ENDPOINT_PREFIX}/stats/", params=params)
        return response
