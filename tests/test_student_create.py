import random

import allure
from faker import Faker

from logger.logger import Logger
from services.university.models.base_student import DegreeEnum
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.university_service import UniversityService

faker = Faker()


class TestStudentCreate:
    @allure.title("Создание студента в существующей группе")
    @allure.feature("Управление студентами")
    @allure.story("Создание студента")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_student_create(self, university_api_utils_admin):
        Logger.info("### Step 1. Create group")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group = GroupRequest(name=faker.name())
        group_response = university_service.create_group(group_request=group)

        Logger.info("### Step 2. Create student")
        student = StudentRequest(first_name=faker.first_name(),
                                 last_name=faker.last_name(),
                                 email=faker.email(),
                                 degree=random.choice([option for option in DegreeEnum]),
                                 phone=faker.numerify("+7##########"),
                                 group_id=group_response.id)
        student_response = university_service.create_student(student_request=student)

        assert student_response.group_id == group_response.id, f"Wrong group id\n" \
                                                               f"Actual: {student_response.group_id}\n" \
                                                               f"Expected: {group_response.id}"
