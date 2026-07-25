from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.core.analysis import AnalysisStageName, AnalysisStatus

NonEmptyText = Annotated[str, Field(min_length=1)]
NonEmptyTextList = Annotated[list[NonEmptyText], Field(min_length=1)]


class BacklogPriority(str, Enum):
    MUST = 'must'
    SHOULD = 'should'
    COULD = 'could'


class RiskLevel(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class AudienceSegment(BaseModel):
    name: NonEmptyText
    description: NonEmptyText
    needs: NonEmptyTextList


class JTBDItem(BaseModel):
    situation: NonEmptyText
    motivation: NonEmptyText
    expected_outcome: NonEmptyText


class LeanCanvas(BaseModel):
    problems: NonEmptyTextList
    customer_segments: NonEmptyTextList
    unique_value_proposition: NonEmptyText
    solutions: NonEmptyTextList
    channels: NonEmptyTextList
    revenue_streams: NonEmptyTextList
    cost_structure: NonEmptyTextList
    key_metrics: NonEmptyTextList
    unfair_advantage: NonEmptyText


class MVPFeature(BaseModel):
    name: NonEmptyText
    description: NonEmptyText
    priority: BacklogPriority


class BacklogItem(BaseModel):
    epic: NonEmptyText
    user_story: NonEmptyText
    acceptance_criteria: NonEmptyTextList
    priority: BacklogPriority


class RoadmapStage(BaseModel):
    name: NonEmptyText
    goal: NonEmptyText
    deliverables: NonEmptyTextList


class ProductRisk(BaseModel):
    description: NonEmptyText
    level: RiskLevel
    mitigation: NonEmptyText


class CriticReview(BaseModel):
    issues: list[NonEmptyText]
    contradictions: list[NonEmptyText]
    recommendations: NonEmptyTextList


class AnalysisReport(BaseModel):
    summary: NonEmptyText
    analysis_plan: NonEmptyTextList
    assumptions: NonEmptyTextList
    problem: NonEmptyText
    target_audience: NonEmptyText
    audience_segments: Annotated[list[AudienceSegment], Field(min_length=1)]
    value_proposition: NonEmptyText
    jtbd: Annotated[list[JTBDItem], Field(min_length=1)]
    lean_canvas: LeanCanvas
    mvp: Annotated[list[MVPFeature], Field(min_length=1)]
    backlog: Annotated[list[BacklogItem], Field(min_length=1)]
    roadmap: Annotated[list[RoadmapStage], Field(min_length=1)]
    risks: Annotated[list[ProductRisk], Field(min_length=1)]
    critic_review: CriticReview
    recommendations: NonEmptyTextList
    final_report_markdown: NonEmptyText


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
    result: AnalysisReport | None
    error_message: str | None
    started_at: datetime | None
    finished_at: datetime | None
    stages: list[AnalysisStageRead]
