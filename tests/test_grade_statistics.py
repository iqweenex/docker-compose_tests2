import random
from faker import Faker

from logger.logger import Logger
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.models.grade_request import GradeRequest
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum
from services.university.university_service import UniversityService

faker = Faker()


class TestGradeStatistics:
    def test_grade_statistics_for_student(self, university_api_utils_admin):
        Logger.info("### Step 1. Create test data")
        university_service = UniversityService(api_utils=university_api_utils_admin)

        # Create group
        group = university_service.create_random_group()

        student_response = university_service.create_random_student(group.id)

        teacher_response = university_service.create_random_teacher()

        Logger.info("### Step 2. Create multiple grades for the student")
        grades = []
        for _ in range(10):
            grade_request = GradeRequest(
                teacher_id=teacher_response.id,
                student_id=student_response.id,
                grade=random.randint(0, 5)
            )
            grade_response = university_service.create_grade(grade_request=grade_request)
            grades.append(grade_response.grade)

        Logger.info("### Step 3. Get grade statistics for the student")
        stats = university_service.get_grades_stats(student_id=student_response.id)

        assert stats.min == min(grades), \
            f"Wrong min.\n" \
            f"Actual: {stats.min}\n" \
            f"Expected: {min(grades)}"

        assert stats.max == max(grades), \
            f"Wrong max.\n" \
            f"Actual: {stats.max}\n" \
            f"Expected: {max(grades)}"

        assert round(stats.avg, 2) == round(sum(grades) / len(grades), 2), \
            f"Wrong avg.\n" \
            f"Actual: {stats.avg}\n" \
            f"Expected: {sum(grades) / len(grades)}"

    def test_grade_statistics_empty(self, university_api_utils_admin):
        Logger.info("### Get statistics for non-existent student")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        stats = university_service.get_grades_stats(student_id=-1)

        assert stats.count == 0, \
            f"Wrong count for empty stats.\n" \
            f"Actual: {stats.count}\n" \
            f"Expected: 0"