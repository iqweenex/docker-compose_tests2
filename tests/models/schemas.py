from pydantic import BaseModel, EmailStr, Field


class DegreeEnum:
    ASSOCIATE = "Associate"
    BACHELOR = "Bachelor"
    MASTER = "Master"
    DOCTORATE = "Doctorate"

    @classmethod
    def all(cls):
        return [cls.ASSOCIATE, cls.BACHELOR, cls.MASTER, cls.DOCTORATE]


class SubjectEnum:
    MATHEMATICS = "Mathematics"
    PHYSICS = "Physics"
    HISTORY = "History"
    BIOLOGY = "Biology"
    GEOGRAPHY = "Geography"

    @classmethod
    def all(cls):
        return [cls.MATHEMATICS, cls.PHYSICS, cls.HISTORY, cls.BIOLOGY, cls.GEOGRAPHY]


class StudentRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    group_id: int
    degree: str = "Bachelor"
    phone: str = Field(pattern=r'^\+\d{11}$')


class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    group_id: int
    degree: str
    phone: str


class GradeRequest(BaseModel):
    student_id: int
    teacher_id: int
    subject: str
    grade: int = Field(ge=2, le=5)


class GradeResponse(BaseModel):
    id: int
    student_id: int
    teacher_id: int
    grade: int
    subject: str | None = None


class StatsResponse(BaseModel):
    count: int
    min: int | None
    max: int | None
    avg: float | None


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class GroupRequest(BaseModel):
    name: str


class GroupResponse(BaseModel):
    id: int
    name: str


class TeacherRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    subject: str
    degree: str = "Bachelor"
    phone: str = Field(pattern=r'^\+\d{11}$')


class TeacherResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    subject: str
    email: str | None = None
    degree: str | None = None
    phone: str | None = None
