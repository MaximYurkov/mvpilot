from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.analysis import AnalysisStageName, AnalysisStatus
from app.core.cases import CaseStage
from app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class Case(Base):
    __tablename__ = 'cases'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    audience: Mapped[str | None] = mapped_column(Text, nullable=True)
    problem: Mapped[str | None] = mapped_column(Text, nullable=True)
    stage: Mapped[str] = mapped_column(
        String(50),
        default=CaseStage.IDEA.value,
        nullable=False,
    )
    analysis_goal: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        onupdate=utc_now,
    )


class AnalysisRun(Base):
    __tablename__ = 'analysis_runs'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    case_id: Mapped[int] = mapped_column(ForeignKey('cases.id'), nullable=False)
    status: Mapped[str] = mapped_column(
        String(50),
        default=AnalysisStatus.PENDING.value,
        nullable=False,
    )
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    stages: Mapped[list['AnalysisStage']] = relationship(
        back_populates='analysis_run',
        cascade='all, delete-orphan',
        order_by='AnalysisStage.position',
        lazy='selectin',
    )


class AnalysisStage(Base):
    __tablename__ = 'analysis_stages'
    __table_args__ = (
        UniqueConstraint(
            'analysis_run_id',
            'name',
            name='uq_analysis_stages_run_name',
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    analysis_run_id: Mapped[int] = mapped_column(
        ForeignKey('analysis_runs.id', ondelete='CASCADE'),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    position: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(
        String(50),
        default=AnalysisStatus.PENDING.value,
        nullable=False,
    )
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    analysis_run: Mapped[AnalysisRun] = relationship(back_populates='stages')
