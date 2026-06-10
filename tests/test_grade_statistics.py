import random
from collections import defaultdict

import allure
import pytest_check as check
from faker import Faker

from logger.logger import Logger
from services.university.models.base_grade import MAX_GRADE, MIN_GRADE
from services.university.models.grade_request import GradeRequest
from services.university.university_service import UniversityService
from utils.soft_assert import SoftAssert

faker = Faker()


class TestGradeStatistics:
    COUNT_GRADES = random.randint(3, 10)
    COUNT_STUDENTS = random.randint(3, 10)
    COUNT_TEACHERS = random.randint(2, 4)

    @allure.title("Статистика оценок для студента")
    @allure.severity(allure.severity_level.NORMAL)
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

    @allure.title("Статистика оценок, проверка фильтрации")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_statistics_for_student_and_teacher(self, university_api_utils_admin):
        Logger.info("### Get statistics for student and teacher")
        university_service = UniversityService(api_utils=university_api_utils_admin)

        Logger.info("### Step 1. Create group")
        with allure.step("Create group"):
            group = university_service.create_random_group()

        Logger.info("### Step 2.1 Create students")
        with allure.step("Create students"):
            students = university_service.create_list_of_students(self.COUNT_STUDENTS, group.id)

        Logger.info("### Step 2.2 Create teachers")
        with allure.step("Create teachers"):
            teachers = university_service.create_list_of_teachers(self.COUNT_TEACHERS)

        Logger.info("### Step 3. Pop one student with some grades")
        with allure.step("Pop one student with some grades"):
            student_for_check = students.pop(0)

            grades_for_check = []
            grades_by_teachers = defaultdict(list)
            for _ in range(self.COUNT_GRADES):
                teacher_id = random.choice(teachers).id
                grade_request = GradeRequest(
                    teacher_id=teacher_id,
                    student_id=student_for_check.id,
                    grade=random.randint(MIN_GRADE, MAX_GRADE)
                )
                grade_response = university_service.create_grade(grade_request=grade_request)
                grades_for_check.append(grade_response.grade)
                grades_by_teachers[teacher_id].append(grade_response.grade)

        Logger.info("### Step 4. Create grades for others students")
        with allure.step("Create other grades"):
            for student in students:
                for _ in range(self.COUNT_GRADES):
                    grade_request = GradeRequest(
                        teacher_id=random.choice(teachers).id,
                        student_id=student.id,
                        grade=random.randint(MIN_GRADE, MAX_GRADE)
                    )
                    university_service.create_grade(grade_request=grade_request)

        Logger.info(f"### Step 5.1. Check grades stats for student_id = {student_for_check.id}")
        with allure.step(f"Check grades statistic for student_id '{student_for_check.id}'"):
            soft_assert = SoftAssert()
            stats = university_service.get_grades_stats(student_id=student_for_check.id)
            self.soft_assert_fast_check_grades(soft_assert, stats, grades_for_check)

        Logger.info(f"### Step 5.2. Check grades stats for student_id = {student_for_check.id} "
                    f"and teacher_id")
        with allure.step(f"Check grades stats for student_id = {student_for_check.id} "
                         f"and teacher_id"):
            for teacher_id in grades_by_teachers.keys():
                grades = grades_by_teachers[teacher_id]
                stats = university_service.get_grades_stats(
                    student_id=student_for_check.id,
                    teacher_id=teacher_id)
                self.soft_assert_fast_check_grades(soft_assert, stats, grades)

    def soft_assert_fast_check_grades(self, soft_assert: SoftAssert, stats, grades_for_check):
        soft_assert.assert_equal(stats.count, len(grades_for_check))
        soft_assert.assert_equal(stats.min, min(grades_for_check))
        soft_assert.assert_equal(stats.max, max(grades_for_check))
        soft_assert.assert_equal(round(stats.avg, 2), round(sum(grades_for_check) / len(grades_for_check), 2))
        soft_assert.assert_all()

    @allure.title("Общая статистика всех оценок")
    @allure.story("Общая статистика")
    @allure.severity(allure.severity_level.MINOR)
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
            "Wrong count for empty stats."

    @allure.title("Статистика для несуществующего студента")
    @allure.severity(allure.severity_level.TRIVIAL)
    def test_grade_statistics_for_non_existent_student(self, university_api_utils_admin):
        Logger.info("### Get statistics for non-existent student")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        stats = university_service.get_grades_stats(student_id=-1)

        Logger.info(f"=====Stats: {stats.model_dump()}")

        soft_assert = SoftAssert()

        soft_assert.assert_equal(stats.count, 0)
        soft_assert.assert_true(stats.min is None)
        soft_assert.assert_true(stats.max is None)
        soft_assert.assert_true(stats.avg is None)
        soft_assert.assert_all()

    @allure.title("Статистика для несуществующего учителя")
    @allure.story("Граничные случаи")
    @allure.severity(allure.severity_level.TRIVIAL)
    def test_grade_statistics_for_non_existent_teacher(self, university_api_utils_admin):
        Logger.info("### Get statistics for non-existent teacher")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        stats = university_service.get_grades_stats(teacher_id=-1)

        Logger.info(f"====Stats: {stats.model_dump()}")

        soft_assert = SoftAssert()

        soft_assert.assert_equal(stats.count, 0)
        soft_assert.assert_true(stats.min is None)
        soft_assert.assert_true(stats.max is None)
        soft_assert.assert_true(stats.avg is None)
        soft_assert.assert_all()

    @allure.title("Статистика для несуществующей группы")
    @allure.story("Граничные случаи")
    @allure.severity(allure.severity_level.TRIVIAL)
    def test_grade_statistics_for_non_existent_group(self, university_api_utils_admin):
        Logger.info("### Get statistics for non-existent group")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        stats = university_service.get_grades_stats(group_id=-1)

        Logger.info(f"====Stats: {stats.model_dump()}")

        assert stats.count == 0, \
            f"Wrong count for empty stats.\n" \
            f"Actual: {stats.count}\n" \
            f"Expected: 0"
