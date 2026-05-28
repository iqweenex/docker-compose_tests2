from tests.helpers.api_client import ApiClient
from tests.helpers.auth_manager import AuthManager
from tests.models.schemas import (
    StudentRequest, StudentResponse,
    GradeRequest, GradeResponse,
    GroupRequest, GroupResponse,
    TeacherRequest, TeacherResponse,
    StatsResponse
)


class UniversityService:
    def __init__(self, api_client: ApiClient, auth_manager: AuthManager):
        self.api_client = api_client
        self.auth_manager = auth_manager

    def _get_auth_headers(self) -> dict:
        return self.auth_manager.get_auth_headers()

    def create_student(self, student: StudentRequest) -> StudentResponse:
        response = self.api_client.post(
            "/students/",
            json_data=student.model_dump(),
            headers=self._get_auth_headers()
        )
        response.raise_for_status()
        return StudentResponse.model_validate(response.json())

    def get_students(self) -> list[StudentResponse]:
        response = self.api_client.get("/students/", headers=self._get_auth_headers())
        response.raise_for_status()
        return [StudentResponse.model_validate(item) for item in response.json()]

    def create_grade(self, grade: GradeRequest) -> GradeResponse:
        response = self.api_client.post(
            "/grades/",
            data=grade.model_dump(),
            headers=self._get_auth_headers()
        )
        response.raise_for_status()
        return GradeResponse.model_validate(response.json())

    def get_stats(self) -> StatsResponse:
        response = self.api_client.get("/grades/stats/", headers=self._get_auth_headers())
        response.raise_for_status()
        return StatsResponse.model_validate(response.json())

    def create_group(self, group: GroupRequest) -> GroupResponse:
        response = self.api_client.post(
            "/groups/",
            json_data=group.model_dump(),
            headers=self._get_auth_headers()
        )
        response.raise_for_status()
        return GroupResponse.model_validate(response.json())

    def create_teacher(self, teacher: TeacherRequest) -> TeacherResponse:
        response = self.api_client.post(
            "/teachers/",
            json_data=teacher.model_dump(),
            headers=self._get_auth_headers()
        )
        response.raise_for_status()
        return TeacherResponse.model_validate(response.json())

    def delete_student(self, student_id: int) -> None:
        response = self.api_client.delete(
            f"/students/{student_id}/",
            headers=self._get_auth_headers()
        )
        response.raise_for_status()

    def delete_grade(self, grade_id: int) -> None:
        response = self.api_client.delete(
            f"/grades/{grade_id}/",
            headers=self._get_auth_headers()
        )
        response.raise_for_status()

    def get_grades(self) -> list[GradeResponse]:
        response = self.api_client.get("/grades/", headers=self._get_auth_headers())
        response.raise_for_status()
        return [GradeResponse.model_validate(item) for item in response.json()]
