from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import Case
from app.db.session import get_db
from app.schemas.cases import CaseCreate, CaseRead

router = APIRouter(prefix='/cases', tags=['cases'])


@router.get('', response_model=list[CaseRead])
def get_cases(db: Session = Depends(get_db)):
    return db.query(Case).order_by(Case.created_at.desc()).all()


@router.post('', response_model=CaseRead, status_code=status.HTTP_201_CREATED)
def create_case(case_data: CaseCreate, db: Session = Depends(get_db)):
    case = Case(**case_data.model_dump())
    db.add(case)
    db.commit()
    db.refresh(case)
    return case


@router.get('/{case_id}', response_model=CaseRead)
def get_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Case not found',
        )

    return case