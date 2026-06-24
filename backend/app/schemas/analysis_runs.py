from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnalysisRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    case_id: int
    status: str
    result: str | None
    error_message: str | None
    started_at: datetime | None
    finished_at: datetime | None