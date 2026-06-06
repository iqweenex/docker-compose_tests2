from services.general.base_service import BaseService
from services.general.models.success_response import SuccessResponse
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentHelper
from services.university.helpers.teacher_helper import TeacherHelper
from services.university.helpers.grade_helper import GradeHelper
from services.university.models.base_grade import BaseGrade, MIN_GRADE, MAX_GRADE
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum
from services.university.models.grade_request import GradeRequest
from services.university.models.grade_response import GradeResponse
from services.university.models.grade_statistics_response import GradeStatisticsResponse
from services.university.models.group_request import GroupRequest
from services.university.models.group_response import GroupResponse
from services.university.models.student_request import StudentRequest
from services.university.models.student_response import StudentResponse
from services.university.models.teacher_request import TeacherRequest
from services.university.models.teacher_response import TeacherResponse
from utils.api_utils import ApiUtils
from faker import Faker
import random

faker = Faker()


class UniversityService(BaseService):
    SERVICE_URL = "http://127.0.0.1:8001"

    def __init__(self, api_utils: ApiUtils):
        super().__init__(api_utils)

        self.group_helper = GroupHelper(self.api_utils)
        self.student_helper = StudentHelper(self.api_utils)
        self.teacher_helper = TeacherHelper(self.api_utils)
        self.grade_helper = GradeHelper(self.api_utils)

    def create_group(self, group_request: GroupRequest) -> GroupResponse:
        response = self.group_helper.post_group(json=group_request.model_dump())
        return GroupResponse(**response.json())

    def create_student(self, student_request: StudentRequest) -> StudentResponse:
        response = self.student_helper.post_student(json=student_request.model_dump())
        return StudentResponse(**response.json())

    def create_teacher(self, teacher_request: TeacherRequest) -> TeacherResponse:
        response = self.teacher_helper.post_teacher(json=teacher_request.model_dump())
        return TeacherResponse(**response.json())

    def create_grade(self, grade_request: GradeRequest) -> GradeResponse:
        response = self.grade_helper.post_grade(data=grade_request.model_dump())
        return GradeResponse(**response.json())

    def update_grade(self, grade_id: int, grade_request: GradeRequest) -> GradeResponse:
        response = self.grade_helper.put_grade(grade_id=grade_id, data=grade_request.model_dump())
        return GradeResponse(**response.json())

    def delete_grade(self, grade_id: int) -> SuccessResponse:
        response = self.grade_helper.delete_grade(grade_id=grade_id)
        return SuccessResponse(**response.json())

    def create_random_student(self, group_id: int):
        student = StudentRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=random.choice([option for option in DegreeEnum]),
            phone=faker.numerify("+7##########"),
            group_id=group_id
        )
        return self.create_student(student_request=student)

    def create_random_group(self) -> GroupResponse:
        group = GroupRequest(name=faker.name())
        return self.create_group(group_request=group)

    def create_random_teacher(self) -> TeacherResponse:
        teacher = TeacherRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            subject=random.choice([option for option in SubjectEnum])
        )
        return self.create_teacher(teacher_request=teacher)

    def create_random_grade(self) -> GradeResponse:
        group = self.create_random_group()
        student = self.create_random_student(group_id=group.id)
        teacher = self.create_random_teacher()

        grade_request = GradeRequest(
            teacher_id=teacher.id,
            student_id=student.id,
            grade=random.randint(MIN_GRADE, MAX_GRADE)
        )
        return self.create_grade(grade_request=grade_request)

    def get_grades_stats(self, student_id: int = None, teacher_id: int = None,
                         group_id: int = None) -> GradeStatisticsResponse:
        response = self.grade_helper.get_grades_stats(
            student_id=student_id,
            teacher_id=teacher_id,
            group_id=group_id
        )
        return GradeStatisticsResponse(**response.json())

    def create_list_of_students(self, students_count, group_id) -> list[StudentResponse]:
        students = []
        for _ in range(students_count):
            students.append(self.create_random_student(group_id))

        return students

    def create_list_of_teachers(self, teachers_count) -> list[TeacherResponse]:
        teachers = []
        for _ in range(teachers_count):
            teachers.append(self.create_random_teacher())

        return teachers

