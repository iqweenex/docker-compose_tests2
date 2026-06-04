import random
from faker import Faker

from services.university.models.base_teacher import SubjectEnum
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService

faker = Faker()


class TestTeacherCreate:
    def test_teacher_create(self, university_api_utils_admin):
        university_service = UniversityService(api_utils=university_api_utils_admin)
        teacher_request = TeacherRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            subject=random.choice([option for option in SubjectEnum])
        )
        teacher_response = university_service.create_teacher(teacher_request=teacher_request)

        assert teacher_request.first_name == teacher_response.first_name, \
            f"Wrong first_name\n" \
            f"Actual: {teacher_response.first_name}\n" \
            f"Expected: {teacher_request.first_name}"

        assert teacher_request.subject == teacher_response.subject, \
            f"Wrong subject\n" \
            f"Actual: {teacher_response.subject}\n" \
            f"Expected: {teacher_request.subject}"
