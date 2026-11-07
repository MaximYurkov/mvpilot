"""Load reference demo data into an empty, already migrated database."""

import json
import sys
from datetime import datetime
from pathlib import Path

backend_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_path))

from app.db.models import AnalysisRun, Case
from app.db.session import SessionLocal
from app.schemas.reports import CaseReport


def seed_demo(db):
    if db.query(Case).first() is not None:
        raise ValueError('База уже содержит кейсы. Демо-данные не добавлены.')

    fixtures = backend_path / 'tests' / 'fixtures'
    cases = json.loads((fixtures / 'cases.json').read_text(encoding='utf-8'))
    reports = json.loads((fixtures / 'reports.json').read_text(encoding='utf-8'))
    for item in cases:
        case = Case(
            id=item['id'],
            title=item['title'],
            description=item['description'],
            audience=item['audience'],
            created_at=datetime.fromisoformat(item['createdAt']),
            updated_at=datetime.fromisoformat(item['updatedAt']),
        )
        db.add(case)
        db.flush()
        payload = reports[str(case.id)]
        if payload is not None:
            report = CaseReport.model_validate(payload)
            db.add(AnalysisRun(
                case_id=case.id,
                status='completed',
                result=report.model_dump(mode='json', exclude_unset=True),
                started_at=case.updated_at,
                finished_at=case.updated_at,
            ))
    db.commit()


if __name__ == '__main__':
    with SessionLocal() as session:
        try:
            seed_demo(session)
        except ValueError as error:
            session.rollback()
            raise SystemExit(str(error)) from error
    print('Добавлены два эталонных кейса и один отчёт.')
