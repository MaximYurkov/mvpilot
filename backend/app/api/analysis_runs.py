from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import AnalysisRun, Case
from app.db.session import get_db
from app.schemas.analysis_runs import AnalysisRunRead

router = APIRouter(tags=['analysis-runs'])


@router.post(
    '/cases/{case_id}/analysis-runs',
    response_model=AnalysisRunRead,
    status_code=status.HTTP_201_CREATED,
)
def create_analysis_run(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Case not found',
        )

    analysis_run = AnalysisRun(case_id=case_id, status='pending')

    db.add(analysis_run)
    db.commit()
    db.refresh(analysis_run)

    return analysis_run


@router.get('/cases/{case_id}/analysis-runs', response_model=list[AnalysisRunRead])
def get_case_analysis_runs(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Case not found',
        )

    return (
        db.query(AnalysisRun)
        .filter(AnalysisRun.case_id == case_id)
        .order_by(AnalysisRun.id.desc())
        .all()
    )


@router.get('/analysis-runs/{run_id}', response_model=AnalysisRunRead)
def get_analysis_run(run_id: int, db: Session = Depends(get_db)):
    analysis_run = db.query(AnalysisRun).filter(AnalysisRun.id == run_id).first()

    if analysis_run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Analysis run not found',
        )

    return analysis_run