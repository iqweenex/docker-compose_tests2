import random

import allure
import pytest_check as check

from logger.logger import Logger
from services.university.models.base_grade import MAX_GRADE, MIN_GRADE
from services.university.models.grade_request import GradeRequest
from services.university.university_service import UniversityService


class TestGradeCreate:
    @allure.title("Создание оценки студента")
    @allure.feature("Управление оценками")
    @allure.severity(allure.severity_level.NORMAL)
    def test_grade_create(self, university_api_utils_admin):
        university_service = UniversityService(api_utils=university_api_utils_admin)
        Logger.info("### Step 1. Create group")
        with allure.step("Create group"):
            group = university_service.create_random_group()

        Logger.info("### Step 2. Create random student")
        with allure.step(f"Create random student with group_id='{group.id}'"):
            student = university_service.create_random_student(group.id)

        Logger.info("### Step 3. Create teacher")
        with allure.step("Create random teacher"):
            teacher = university_service.create_random_teacher()

        Logger.info("### Step 4. Create grade")
        with allure.step("Create grade"):
            grade_request = GradeRequest(
                teacher_id=teacher.id,
                student_id=student.id,
                grade=random.randint(MIN_GRADE, MAX_GRADE)
            )
            grade_response = university_service.create_grade(grade_request=grade_request)

        check.equal(
            grade_response.teacher_id,
            teacher.id,
            f"Wrong teacher_id."
            f"\nActual: {grade_response.teacher_id}\n"
            f"Expected: {teacher.id}"
        )

        check.equal(
            grade_response.student_id,
            student.id,
            f"Wrong student_id.\n"
            f"Actual: {grade_response.student_id}\n"
            f"Expected: {student.id}"
        )

        check.equal(
            grade_response.grade,
            grade_request.grade,
            f"Wrong grade.\n"
            f"Actual: {grade_response.grade}\n"
            f"Expected: {grade_request.grade}"
        )

    @allure.title("Создание и обновление оценки")
    @allure.feature("Управление оценками")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_and_update_grade(self, university_api_utils_admin):
        university_service = UniversityService(api_utils=university_api_utils_admin)
        Logger.info("### Step 1. Create random grade")
        with allure.step("Create random grade"):
            grade = university_service.create_random_grade()
        actual_grade = grade.grade
        new_grade = actual_grade - 1 if actual_grade == 5 else actual_grade + 1

        Logger.info("### Step 2. Update grade")
        with allure.step("Update grade"):
            grade_request = GradeRequest(
                teacher_id=grade.teacher_id,
                student_id=grade.student_id,
                grade=new_grade
            )

            updated_grade = university_service.update_grade(
                grade_id=grade.id,
                grade_request=grade_request
            )

        check.equal(
            updated_grade.grade,
            new_grade,
            f"Wrong grade\n"
            f"Actual: {updated_grade.grade}\n"
            f"Expected: {new_grade}")

        check.equal(
            updated_grade.id,
            grade.id,
            f"Wrong id\n"
            f"Actual: {updated_grade.id}\n"
            f"Expected: {grade.id}")
