import unittest
from unittest.mock import patch

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.analysis_runs import (
    create_analysis_run,
    get_analysis_run,
    get_case_analysis_runs,
)
from app.core.analysis import AnalysisStatus
from app.db.base import Base
from app.db.models import AnalysisRun, Case


class AnalysisRunsTestCase(unittest.TestCase):
    def setUp(self):
        engine = create_engine(
            'sqlite://',
            connect_args={'check_same_thread': False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(bind=engine)
        self.engine = engine
        self.db = sessionmaker(bind=engine)()

        case = Case(
            title='Сервис планирования питания',
            description='Помогает составлять меню на неделю.',
            audience='Занятые люди',
            problem='Не хватает времени на планирование рациона',
        )
        self.db.add(case)
        self.db.commit()
        self.db.refresh(case)
        self.case = case

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def test_analysis_run_is_completed_and_can_be_read(self):
        created_run = create_analysis_run(self.case.id, self.db)

        self.assertEqual(created_run.status, AnalysisStatus.COMPLETED.value)
        self.assertIsNotNone(created_run.started_at)
        self.assertIsNotNone(created_run.finished_at)
        self.assertEqual(
            created_run.result['target_audience'],
            self.case.audience,
        )

        fetched_run = get_analysis_run(created_run.id, self.db)
        case_runs = get_case_analysis_runs(self.case.id, self.db)

        self.assertEqual(fetched_run.id, created_run.id)
        self.assertEqual([run.id for run in case_runs], [created_run.id])

    def test_unknown_case_returns_404(self):
        with self.assertRaises(HTTPException) as error:
            create_analysis_run(999, self.db)

        self.assertEqual(error.exception.status_code, 404)

    def test_unknown_analysis_run_returns_404(self):
        with self.assertRaises(HTTPException) as error:
            get_analysis_run(999, self.db)

        self.assertEqual(error.exception.status_code, 404)

    def test_analyzer_error_is_saved_as_failed(self):
        with patch(
            'app.api.analysis_runs.build_mock_report',
            side_effect=RuntimeError('Test analyzer error'),
        ):
            with self.assertRaises(HTTPException) as error:
                create_analysis_run(self.case.id, self.db)

        failed_run = self.db.query(AnalysisRun).one()

        self.assertEqual(error.exception.status_code, 500)
        self.assertEqual(failed_run.status, AnalysisStatus.FAILED.value)
        self.assertEqual(failed_run.error_message, 'Test analyzer error')
        self.assertIsNotNone(failed_run.finished_at)


if __name__ == '__main__':
    unittest.main()
