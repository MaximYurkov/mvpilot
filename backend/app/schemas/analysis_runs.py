from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.core.analysis import AnalysisStageName, AnalysisStatus
from app.schemas.reports import CaseReport


class AnalysisStageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: AnalysisStageName
    position: int
    status: AnalysisStatus
    result: dict[str, object] | None
    error_message: str | None
    started_at: datetime | None
    finished_at: datetime | None


class AnalysisRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    case_id: int
    status: AnalysisStatus
    result: CaseReport | None
    error_message: str | None
    started_at: datetime | None
    finished_at: datetime | None
    stages: list[AnalysisStageRead]
