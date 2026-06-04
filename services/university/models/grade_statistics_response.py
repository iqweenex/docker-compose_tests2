from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from .base_grade import MAX_GRADE, MIN_GRADE


class GradeStatisticsResponse(BaseModel):
    model_config = ConfigDict(extra='forbid')

    count: int = Field(ge=0, description="Total number of grades")
    min: Optional[int] = Field(ge=MIN_GRADE, le=MAX_GRADE, description="Minimum grade value")
    max: Optional[int] = Field(ge=MIN_GRADE, le=MAX_GRADE, description="Maximum grade value")
    avg: Optional[float] = Field(ge=MIN_GRADE, le=MAX_GRADE, description="Average grade value")
