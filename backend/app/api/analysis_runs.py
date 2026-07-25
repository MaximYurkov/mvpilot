from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.analysis import AnalysisStatus
from app.db.models import AnalysisRun, Case
from app.db.session import get_db
from app.schemas.analysis_runs import AnalysisRunRead
from app.services.analysis import build_mock_report

router = APIRouter(tags=['analysis-runs'])


def utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def get_case_or_404(case_id: int, db: Session) -> Case:
    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Case not found',
        )

    return case


@router.post(
    '/cases/{case_id}/analysis-runs',
    response_model=AnalysisRunRead,
    status_code=status.HTTP_201_CREATED,
)
def create_analysis_run(case_id: int, db: Session = Depends(get_db)):
    case = get_case_or_404(case_id, db)
    analysis_run = AnalysisRun(case_id=case.id)

    try:
        db.add(analysis_run)
        db.commit()
        db.refresh(analysis_run)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Could not create analysis run',
        ) from exc

    try:
        analysis_run.status = AnalysisStatus.RUNNING.value
        analysis_run.started_at = utc_now()
        db.commit()

        report = build_mock_report(case)

        analysis_run.status = AnalysisStatus.COMPLETED.value
        analysis_run.result = report.model_dump()
        analysis_run.finished_at = utc_now()
        db.commit()
        db.refresh(analysis_run)
    except Exception as exc:
        db.rollback()

        failed_run = db.get(AnalysisRun, analysis_run.id)
        if failed_run is not None:
            failed_run.status = AnalysisStatus.FAILED.value
            failed_run.error_message = str(exc) or type(exc).__name__
            failed_run.finished_at = utc_now()

            try:
                db.commit()
            except SQLAlchemyError:
                db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Analysis failed',
        ) from exc

    return analysis_run


@router.get(
    '/cases/{case_id}/analysis-runs',
    response_model=list[AnalysisRunRead],
)
def get_case_analysis_runs(case_id: int, db: Session = Depends(get_db)):
    get_case_or_404(case_id, db)

    return (
        db.query(AnalysisRun)
        .filter(AnalysisRun.case_id == case_id)
        .order_by(AnalysisRun.id.desc())
        .all()
    )


@router.get('/analysis-runs/{run_id}', response_model=AnalysisRunRead)
def get_analysis_run(run_id: int, db: Session = Depends(get_db)):
    analysis_run = db.get(AnalysisRun, run_id)

    if analysis_run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Analysis run not found',
        )

    return analysis_run
