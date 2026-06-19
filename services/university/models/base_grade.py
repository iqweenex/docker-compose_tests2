from pydantic import BaseModel, ConfigDict, Field

MIN_GRADE = 0
MAX_GRADE = 5


class BaseGrade(BaseModel):
    model_config = ConfigDict(extra='forbid')

    teacher_id: int
    student_id: int
    grade: int = Field(ge=MIN_GRADE, le=MAX_GRADE, description=f"Grade from {MIN_GRADE} to {MIN_GRADE} ")
