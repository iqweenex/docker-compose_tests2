from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class GradeStatisticsResponse(BaseModel):
    model_config = ConfigDict(extra='forbid')

    count: int = Field(ge=0, description="Total number of grades")
    min: Optional[int] = Field(ge=0, le=5, description="Minimum grade value")
    max: Optional[int] = Field(ge=0, le=5, description="Maximum grade value")
    avg: Optional[float] = Field(ge=0, le=5, description="Average grade value")