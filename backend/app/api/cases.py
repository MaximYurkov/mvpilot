from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db.models import Case
from app.db.session import get_db
from app.schemas.cases import CaseCreate, CaseRead, CaseUpdate
from app.schemas.errors import ErrorResponse

router = APIRouter(prefix='/cases', tags=['cases'])


@router.get('', response_model=list[CaseRead], operation_id='listCases')
def get_cases(db: Session = Depends(get_db)):
    return db.query(Case).order_by(Case.created_at.desc()).all()


@router.post(
    '',
    response_model=CaseRead,
    status_code=status.HTTP_201_CREATED,
    operation_id='createCase',
)
def create_case(case_data: CaseCreate, db: Session = Depends(get_db)):
    case = Case(**case_data.model_dump())
    db.add(case)
    db.commit()
    db.refresh(case)
    return case


@router.get(
    '/{case_id}',
    response_model=CaseRead,
    operation_id='getCase',
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorResponse,
            'description': 'Case not found',
        },
    },
)
def get_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Case not found',
        )

    return case


@router.patch(
    '/{case_id}',
    response_model=CaseRead,
    operation_id='updateCase',
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorResponse,
            'description': 'Case not found',
        },
    },
)
def update_case(case_id: int, case_data: CaseUpdate, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Case not found',
        )

    update_data = case_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(case, field, value)

    db.commit()
    db.refresh(case)

    return case


@router.delete(
    '/{case_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id='deleteCase',
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorResponse,
            'description': 'Case not found',
        },
    },
)
def delete_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Case not found',
        )

    db.delete(case)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
