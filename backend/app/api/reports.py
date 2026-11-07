from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import JSON
from sqlalchemy.orm import Session

from app.core.analysis import AnalysisStatus
from app.db.models import AnalysisRun, Case
from app.db.session import get_db
from app.schemas.errors import ErrorResponse
from app.schemas.reports import CaseReport

router = APIRouter(tags=['reports'])


def latest_case_report(case_id: int, db: Session) -> CaseReport | None:
    run = (
        db.query(AnalysisRun)
        .filter(
            AnalysisRun.case_id == case_id,
            AnalysisRun.status == AnalysisStatus.COMPLETED.value,
            AnalysisRun.result.is_not(None),
            AnalysisRun.result != JSON.NULL,
        )
        .order_by(AnalysisRun.id.desc())
        .first()
    )
    return None if run is None else CaseReport.model_validate(run.result)


@router.get(
    '/cases/{case_id}/report',
    response_model=CaseReport | None,
    operation_id='getCaseReport',
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorResponse,
            'description': 'Case not found',
        },
    },
)
def get_case_report(case_id: int, db: Session = Depends(get_db)):
    if db.get(Case, case_id) is None:
        raise HTTPException(status_code=404, detail='Case not found')
    return latest_case_report(case_id, db)


@router.get(
    '/reports',
    response_model=dict[str, CaseReport | None],
    operation_id='listReports',
)
def list_reports(db: Session = Depends(get_db)):
    """The same ID-to-report map shape as the frontend reports.json fixture."""
    return {
        str(case.id): latest_case_report(case.id, db)
        for case in db.query(Case).order_by(Case.id).all()
    }
