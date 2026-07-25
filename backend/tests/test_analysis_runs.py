import unittest
from unittest.mock import patch

from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.analysis_runs import (
    create_analysis_run,
    get_analysis_run,
    get_case_analysis_runs,
)
from app.core.analysis import AnalysisStageName, AnalysisStatus
from app.core.cases import CaseStage
from app.db.base import Base
from app.db.models import AnalysisRun, AnalysisStage, Case
from app.schemas.analysis_runs import AnalysisReport


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
            stage=CaseStage.PROTOTYPE.value,
            analysis_goal='Проверить состав MVP',
        )
        self.db.add(case)
        self.db.commit()
        self.db.refresh(case)
        self.case = case

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def test_completed_run_contains_full_valid_report(self):
        created_run = create_analysis_run(self.case.id, self.db)
        report = AnalysisReport.model_validate(created_run.result)

        self.assertEqual(created_run.status, AnalysisStatus.COMPLETED.value)
        self.assertIsNotNone(created_run.started_at)
        self.assertIsNotNone(created_run.finished_at)
        self.assertEqual(report.target_audience, self.case.audience)
        self.assertGreaterEqual(len(report.jtbd), 1)
        self.assertGreaterEqual(len(report.mvp), 1)
        self.assertGreaterEqual(len(report.backlog), 1)
        self.assertGreaterEqual(len(report.roadmap), 1)
        self.assertGreaterEqual(len(report.risks), 1)
        self.assertIn('прототип', report.summary)
        self.assertIn('Проверить состав MVP', report.analysis_plan[0])
        self.assertIn('## Lean Canvas', report.final_report_markdown)
        self.assertIn('## Критика', report.final_report_markdown)
        self.assertEqual(
            [stage.name for stage in created_run.stages],
            [stage_name.value for stage_name in AnalysisStageName],
        )

        for position, stage in enumerate(created_run.stages, start=1):
            self.assertEqual(stage.position, position)
            self.assertEqual(stage.status, AnalysisStatus.COMPLETED.value)
            self.assertIsNotNone(stage.result)
            self.assertIsNotNone(stage.started_at)
            self.assertIsNotNone(stage.finished_at)
            self.assertIsNone(stage.error_message)

        fetched_run = get_analysis_run(created_run.id, self.db)
        case_runs = get_case_analysis_runs(self.case.id, self.db)

        self.assertEqual(fetched_run.id, created_run.id)
        self.assertEqual(len(fetched_run.stages), 5)
        self.assertEqual([run.id for run in case_runs], [created_run.id])
        self.assertEqual(len(case_runs[0].stages), 5)

    def test_report_contract_rejects_missing_sections(self):
        with self.assertRaises(ValidationError):
            AnalysisReport.model_validate({'summary': 'Неполный отчёт'})

    def test_report_contract_rejects_empty_required_lists(self):
        created_run = create_analysis_run(self.case.id, self.db)
        invalid_result = {**created_run.result, 'jtbd': []}

        with self.assertRaises(ValidationError):
            AnalysisReport.model_validate(invalid_result)

    def test_missing_case_details_are_marked_as_hypotheses(self):
        incomplete_case = Case(
            title='Новая идея',
            description='Краткое описание идеи.',
            audience=None,
            problem=None,
        )
        self.db.add(incomplete_case)
        self.db.commit()
        self.db.refresh(incomplete_case)

        created_run = create_analysis_run(incomplete_case.id, self.db)
        report = AnalysisReport.model_validate(created_run.result)

        self.assertIn('ещё не определён', report.target_audience)
        self.assertIn('требует уточнения', report.problem)
        self.assertGreaterEqual(len(report.critic_review.issues), 4)
        self.assertGreaterEqual(len(report.risks), 5)

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
        failed_stages = (
            self.db.query(AnalysisStage)
            .order_by(AnalysisStage.position)
            .all()
        )

        self.assertEqual(error.exception.status_code, 500)
        self.assertEqual(failed_run.status, AnalysisStatus.FAILED.value)
        self.assertEqual(failed_run.error_message, 'Test analyzer error')
        self.assertIsNotNone(failed_run.finished_at)
        self.assertEqual(len(failed_stages), 5)
        self.assertEqual(failed_stages[0].name, AnalysisStageName.PLANNER.value)
        self.assertEqual(
            failed_stages[0].status,
            AnalysisStatus.FAILED.value,
        )
        self.assertEqual(failed_stages[0].error_message, 'Test analyzer error')

        for pending_stage in failed_stages[1:]:
            self.assertEqual(
                pending_stage.status,
                AnalysisStatus.PENDING.value,
            )
            self.assertIsNone(pending_stage.started_at)


if __name__ == '__main__':
    unittest.main()
