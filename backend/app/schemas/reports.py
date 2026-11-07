"""Report contract matching the frontend domain types, including nullable fields."""

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel

from app.schemas.legacy_reports import upgrade_legacy_report


class ReportModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        serialize_by_alias=True,
        extra='forbid',
    )


class Priority(str, Enum):
    MUST = 'must'
    SHOULD = 'should'
    COULD = 'could'
    WONT = 'wont'


class JtbdPriority(str, Enum):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'


class SectionStatus(str, Enum):
    READY = 'ready'
    PARTIAL = 'partial'
    INSUFFICIENT_DATA = 'insufficient_data'
    NOT_APPLICABLE = 'not_applicable'


class Source(ReportModel):
    id: str
    title: str
    url: str | None
    publisher: str | None
    published_at: str | None


class SectionMeta(ReportModel):
    status: SectionStatus
    note: str | None
    sources: list[Source]


class MetricNode(ReportModel):
    name: str
    children: list['MetricNode'] = Field(default_factory=list)


class MarketSize(ReportModel):
    value: float
    unit: str
    label: str


class Competitor(ReportModel):
    name: str
    x: float | None
    y: float | None
    is_product: bool
    url: str | None
    strengths: list[str]
    weaknesses: list[str]


class FeatureComparison(ReportModel):
    feature: str
    product: bool
    competitor1: bool
    competitor2: bool
    competitor3: bool


class Risk(ReportModel):
    cell: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9]
    description: str
    mitigation: str
    cheap_check: str


class FinanceFigure(ReportModel):
    key: str
    label: str
    value: float | None
    unit: str
    note: str | None


class BudgetSection(ReportModel):
    name: str
    recommended: float
    minimum: float


class Readiness(ReportModel):
    axis: str
    score: float
    comment: str


class OverviewTile(ReportModel):
    label: str
    value: float
    unit: str


class Overview(SectionMeta):
    idea: str
    readiness: list[Readiness]
    tiles: list[OverviewTile]


class MarketDynamics(ReportModel):
    year: float
    value: float


class MarketTrend(ReportModel):
    name: str
    direction: Literal['up', 'flat', 'down']
    comment: str


class Market(SectionMeta):
    tam: MarketSize | None
    sam: MarketSize | None
    som: MarketSize | None
    method: Literal['bottom-up', 'top-down'] | None
    method_comment: str | None
    assumptions: list[str]
    dynamics: list[MarketDynamics]
    dynamics_source: str | None
    trends: list[MarketTrend]


class AudienceSegment(ReportModel):
    name: str
    estimated_share: float | None
    description: str
    needs: list[str]


class JtbdItem(ReportModel):
    situation: str
    motivation: str
    outcome: str
    priority: JtbdPriority


class Audience(SectionMeta):
    primary_segment: str | None
    segments: list[AudienceSegment]
    jtbd: list[JtbdItem]


class CompetitorAxes(ReportModel):
    x: str
    y: str


class Swot(ReportModel):
    strengths: list[str]
    weaknesses: list[str]
    opportunities: list[str]
    threats: list[str]


class Competitors(SectionMeta):
    axes: CompetitorAxes
    items: list[Competitor]
    comparison: list[FeatureComparison]
    swot: Swot


class LeanCanvas(SectionMeta):
    problems: list[str]
    solutions: list[str]
    value: str
    advantage: str
    segments: list[str]
    metrics: list[str]
    channels: list[str]
    costs: list[str]
    revenue: list[str]


class MvpFeature(ReportModel):
    name: str
    description: str
    priority: Priority


class UserFlowStep(ReportModel):
    step: str
    description: str


class Mvp(SectionMeta):
    features: list[MvpFeature]
    user_flow: list[UserFlowStep]


class RoadmapStage(ReportModel):
    name: str
    goal: str
    start_month: float
    duration: float
    results: list[str]


class Roadmap(SectionMeta):
    stages: list[RoadmapStage]


class NorthStar(ReportModel):
    name: str
    value: float | None
    unit: str


class FunnelStage(ReportModel):
    stage: str
    value: float
    target: float | None


class Metrics(SectionMeta):
    north_star: NorthStar
    tree: MetricNode | None
    funnel: list[FunnelStage]


class Finance(SectionMeta):
    figures: list[FinanceFigure]
    recommended_total: float | None
    budget_sections: list[BudgetSection]


class Risks(SectionMeta):
    items: list[Risk]


class Partner(ReportModel):
    name: str
    note: str
    url: str | None


class NextStep(ReportModel):
    title: str
    description: str
    priority: Priority
    effort: Literal['low', 'medium', 'high']
    partner: Partner | None


class NextSteps(SectionMeta):
    items: list[NextStep]


class CaseReport(ReportModel):
    overview: Overview
    market: Market
    audience: Audience
    competitors: Competitors
    lean_canvas: LeanCanvas
    mvp: Mvp
    roadmap: Roadmap
    metrics: Metrics
    finance: Finance
    risks: Risks
    next_steps: NextSteps
    markdown: str | None

    @model_validator(mode='before')
    @classmethod
    def accept_persisted_legacy_report(cls, value):
        if (
            isinstance(value, dict)
            and 'overview' not in value
            and 'summary' in value
            and 'final_report_markdown' in value
        ):
            return upgrade_legacy_report(value)
        return value
