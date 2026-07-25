from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.analysis import AnalysisStatus


class AnalysisReport(BaseModel):
    summary: str
    target_audience: str
    problem: str
    strengths: list[str]
    risks: list[str]
    recommendations: list[str]


class AnalysisRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    case_id: int
    status: AnalysisStatus
    result: AnalysisReport | None
    error_message: str | None
    started_at: datetime | None
    finished_at: datetime | None
