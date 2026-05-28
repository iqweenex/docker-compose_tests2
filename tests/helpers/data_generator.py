from faker import Faker
from tests.models.schemas import StudentRequest, GradeRequest, TeacherRequest, GroupRequest
from tests.models.schemas import SubjectEnum, DegreeEnum


class DataGenerator:
    def __init__(self):
        self.faker = Faker()

    def student(self, group_id: int) -> StudentRequest:
        phone = f"+7{self.faker.random_number(digits=10, fix_len=True)}"
        return StudentRequest(
            first_name=self.faker.first_name(),
            last_name=self.faker.last_name(),
            email=self.faker.unique.email(),
            group_id=group_id,
            degree="Bachelor",
            phone=phone
        )

    def grade(self, student_id: int, teacher_id: int) -> GradeRequest:
        return GradeRequest(
            student_id=student_id,
            teacher_id=teacher_id,
            subject=self.faker.random_element(SubjectEnum.all()),
            grade=self.faker.random_int(min=2, max=5)
        )

    def unique_credentials(self) -> dict:
        return {
            "username": self.faker.unique.user_name(),
            "password": self.faker.password(length=12)
        }

    def group(self) -> GroupRequest:
        return GroupRequest(
            name=f"Group-{self.faker.unique.word().title()}"
        )

    def teacher(self) -> TeacherRequest:
        phone = f"+7{self.faker.random_number(digits=10, fix_len=True)}"
        return TeacherRequest(
            first_name=self.faker.first_name(),
            last_name=self.faker.last_name(),
            email=self.faker.unique.email(),
            subject=self.faker.random_element(SubjectEnum.all()),
            degree=self.faker.random_element(DegreeEnum.all()),
            phone=phone
        )
