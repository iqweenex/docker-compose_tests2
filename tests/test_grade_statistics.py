import random
from faker import Faker
import pytest_check as check
from logger.logger import Logger
from services.university.models.base_grade import MAX_GRADE, MIN_GRADE
from services.university.models.grade_request import GradeRequest
from services.university.university_service import UniversityService

faker = Faker()


class TestGradeStatistics:
    COUNT_GRADES = 10

    def test_grade_statistics_for_student(self, university_api_utils_admin):
        Logger.info("### Step 1. Create test data")
        university_service = UniversityService(api_utils=university_api_utils_admin)

        # Create group
        group = university_service.create_random_group()

        student_response = university_service.create_random_student(group.id)

        teacher_response = university_service.create_random_teacher()

        Logger.info("### Step 2. Create multiple grades for the student")
        grades = []
        for _ in range(self.COUNT_GRADES):
            grade_request = GradeRequest(
                teacher_id=teacher_response.id,
                student_id=student_response.id,
                grade=random.randint(MIN_GRADE, MAX_GRADE)
            )
            grade_response = university_service.create_grade(grade_request=grade_request)
            grades.append(grade_response.grade)

        Logger.info("### Step 3. Get grade statistics for the student")
        stats = university_service.get_grades_stats(student_id=student_response.id)
        avg_grades = sum(grades) / len(grades)

        check.equal(
            stats.min,
            min(grades),
            f"Wrong min."
            f"\nActual: {stats.min}\n"
            f"Expected: {min(grades)}"
        )

        check.equal(
            stats.max,
            max(grades),
            f"Wrong max."
            f"\nActual: {stats.max}\n"
            f"Expected: {max(grades)}"
        )

        check.equal(
            round(stats.avg, 2),
            round(avg_grades, 2),
            f"Wrong avg."
            f"\nActual: {stats.avg}\n"
            f"Expected: {avg_grades}"
        )

    def test_get_statictics_for_student_and_teacher(self, university_api_utils_admin):
        Logger.info("### Get statistics for student and teacher")
        Logger.info("### Step 1. Create test data")
        university_service = UniversityService(api_utils=university_api_utils_admin)

        group = university_service.create_random_group()

        student_response = university_service.create_random_student(group.id)

        teacher_response = university_service.create_random_teacher()

        Logger.info("### Step 2. Create multiple grades for the student")
        grades = []
        for _ in range(self.COUNT_GRADES):
            grade_request = GradeRequest(
                teacher_id=teacher_response.id,
                student_id=student_response.id,
                grade=random.randint(MIN_GRADE, MAX_GRADE)
            )
            grade_response = university_service.create_grade(grade_request=grade_request)
            grades.append(grade_response.grade)

        Logger.info("### Step 3. Get grade statistics for the student")
        stats = university_service.get_grades_stats(
            student_id=student_response.id,
            teacher_id=teacher_response.id)

        avg_grades = sum(grades) / len(grades)

        check.equal(
            stats.min,
            min(grades),
            f"Wrong min."
            f"\nActual: {stats.min}\n"
            f"Expected: {min(grades)}"
        )

        check.equal(
            stats.max,
            max(grades),
            f"Wrong max."
            f"\nActual: {stats.max}\n"
            f"Expected: {max(grades)}"
        )

        check.equal(
            round(stats.avg, 2),
            round(avg_grades, 2),
            f"Wrong avg."
            f"\nActual: {stats.avg}\n"
            f"Expected: {avg_grades}"
        )

    def test_grade_statistics_for_empty_params(self, university_api_utils_admin):
        Logger.info("### Get statistics for empty params")
        Logger.info("### Step 1. Create test data")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group = university_service.create_random_group()

        student_response = university_service.create_random_student(group.id)

        teacher_response = university_service.create_random_teacher()

        Logger.info("### Step 2. Create multiple grades for the student")
        grades = []
        for _ in range(self.COUNT_GRADES):
            grade_request = GradeRequest(
                teacher_id=teacher_response.id,
                student_id=student_response.id,
                grade=random.randint(MIN_GRADE, MAX_GRADE)
            )
            grade_response = university_service.create_grade(grade_request=grade_request)
            grades.append(grade_response.grade)

        Logger.info("### Step 3. Get grade statistics for empty params")

        stats = university_service.get_grades_stats()

        Logger.info(f"=====Stats: {stats.model_dump()}")

        assert stats.count > 0, \
            f"Wrong count for empty stats."

    def test_grade_statistics_for_non_existent_student(self, university_api_utils_admin):
        Logger.info("### Get statistics for non-existent student")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        stats = university_service.get_grades_stats(student_id=-1)

        Logger.info(f"=====Stats: {stats.model_dump()}")

        assert stats.count == 0, \
            f"Wrong count for empty stats.\n" \
            f"Actual: {stats.count}\n" \
            f"Expected: 0"

    def test_grade_statistics_for_non_existent_teacher(self, university_api_utils_admin):
        Logger.info("### Get statistics for non-existent teacher")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        stats = university_service.get_grades_stats(teacher_id=-1)

        Logger.info(f"====Stats: {stats.model_dump()}")

        assert stats.count == 0, \
            f"Wrong count for empty stats.\n" \
            f"Actual: {stats.count}\n" \
            f"Expected: 0"

    def test_grade_statistics_for_non_existent_group(self, university_api_utils_admin):
        Logger.info("### Get statistics for non-existent group")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        stats = university_service.get_grades_stats(group_id=-1)

        Logger.info(f"====Stats: {stats.model_dump()}")

        assert stats.count == 0, \
            f"Wrong count for empty stats.\n" \
            f"Actual: {stats.count}\n" \
            f"Expected: 0"
