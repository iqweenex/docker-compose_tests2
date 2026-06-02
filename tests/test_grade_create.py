import random

from logger.logger import Logger
from services.university.university_service import UniversityService
from services.university.models.grade_request import GradeRequest


class TestGradeCreate:
    def test_grade_create_and_update(self, university_api_utils_admin):
        university_service = UniversityService(api_utils=university_api_utils_admin)
        Logger.info(f"### Step 1. Group create")
        group = university_service.create_random_group()

        Logger.info(f"### Step 2. Create random student")
        student = university_service.create_random_student(group.id)

        Logger.info(f"### Step 3. Create teacher")
        teacher = university_service.create_random_teacher()

        grade_request = GradeRequest(
            teacher_id=teacher.id,
            student_id=student.id,
            grade=random.randint(0, 5)
        )
        grade_response = university_service.create_grade(grade_request=grade_request)

        assert grade_response.teacher_id == teacher.id, \
            f"Wrong teacher_id.\n" \
            f"Actual: {grade_response.teacher_id}\n" \
            f"Expected: {teacher.id}"

        assert grade_response.student_id == student.id, \
            f"Wrong student_id.\n" \
            f"Actual: {grade_response.student_id}\n" \
            f"Expected: {student.id}"

        assert grade_response.grade == grade_request.grade, \
            f"Wrong grade.\n" \
            f"Actual: {grade_response.grade}\n" \
            f"Expected: {grade_request.grade}"

    def create_and_update_grade(self, university_api_utils_admin):
        university_service = UniversityService(api_utils=university_api_utils_admin)
        Logger.info(f"### Step 1. Create random grade")
        grade = university_service.create_random_grade()
        actual_grade = grade.grade
        new_grade = actual_grade - 1 if actual_grade == 5 else actual_grade + 1

        Logger.info(f"### Step 2. Update grade")
        grade_request = GradeRequest(
            teacher_id=grade.teacher_id,
            student_id=grade.student_id,
            grade=new_grade
        )

        updated_grade = university_service.update_grade(
            grade_id=grade.id,
            grade_request=grade_request
        )

        assert updated_grade.grade == new_grade, \
            f"Grade not updated.\n" \
            f"Actual: {updated_grade.grade}\n" \
            f"Expected: {new_grade}"

        assert updated_grade.id == grade.id, \
            f"Grade id changed.\n" \
            f"Actual: {updated_grade.id}\n" \
            f"Expected: {grade.id}"
