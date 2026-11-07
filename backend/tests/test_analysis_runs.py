from unittest.mock import patch

from pydantic import ValidationError

from app.core.analysis import AnalysisStageName, AnalysisStatus
from app.db.models import AnalysisRun, AnalysisStage
from app.schemas.reports import CaseReport
from tests.support import APITestCase, fixture


class AnalysisRunsTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.case = self.create_case()

    def run_analysis(self, case_id=None):
        response = self.client.post(
            f"/api/cases/{case_id or self.case['id']}/analysis-runs",
        )
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()

    def test_completed_run_contains_frontend_report_and_five_stages(self):
        run = self.run_analysis()
        report = CaseReport.model_validate(run['result'])
        self.assertEqual(run['status'], 'completed')
        self.assertIsNotNone(run['started_at'])
        self.assertIsNotNone(run['finished_at'])
        self.assertIn(self.case['title'], report.overview.idea)
        self.assertEqual(report.audience.primary_segment, self.case['audience'])
        self.assertIn('## Lean Canvas', report.markdown)
        self.assertEqual(
            [stage['name'] for stage in run['stages']],
            [name.value for name in AnalysisStageName],
        )
        for position, stage in enumerate(run['stages'], start=1):
            self.assertEqual(stage['position'], position)
            self.assertEqual(stage['status'], 'completed')
            self.assertIsNotNone(stage['result'])
            self.assertIsNotNone(stage['started_at'])
            self.assertIsNotNone(stage['finished_at'])
            self.assertIsNone(stage['error_message'])

        self.assertEqual(
            self.client.get(f"/api/analysis-runs/{run['id']}").json(), run,
        )
        self.assertEqual(
            self.client.get(
                f"/api/cases/{self.case['id']}/analysis-runs",
            ).json(),
            [run],
        )

    def test_missing_sections_and_invalid_literals_are_rejected(self):
        with self.assertRaises(ValidationError):
            CaseReport.model_validate({'overview': {'idea': 'Неполный отчёт'}})
        payload = fixture('reports.json')['1']
        payload['risks']['items'][0]['cell'] = 10
        with self.assertRaises(ValidationError):
            CaseReport.model_validate(payload)
        payload = fixture('reports.json')['1']
        payload['mvp']['features'][0]['priority'] = 'urgent'
        with self.assertRaises(ValidationError):
            CaseReport.model_validate(payload)

    def test_nullable_fields_are_required_and_empty_lists_are_valid(self):
        run = self.run_analysis()
        payload = run['result']
        self.assertEqual(payload['market']['dynamics'], [])
        self.assertIsNone(payload['market']['tam'])
        payload['market'].pop('tam')
        with self.assertRaises(ValidationError):
            CaseReport.model_validate(payload)

    def test_missing_numbers_are_not_fabricated(self):
        payload = self.run_analysis()['result']
        self.assertEqual(payload['market']['status'], 'insufficient_data')
        self.assertIsNone(payload['market']['tam'])
        self.assertIsNone(payload['finance']['recommendedTotal'])
        self.assertIsNone(payload['metrics']['northStar']['value'])
        self.assertEqual(payload['overview']['readiness'], [])
        self.assertEqual(payload['overview']['tiles'], [])
        for section in payload.values():
            if isinstance(section, dict) and 'status' in section:
                self.assertEqual(section['sources'], [])
                self.assertIsInstance(section['note'], str)

    def test_report_is_null_before_analysis_and_404_for_unknown_case(self):
        response = self.client.get(f"/api/cases/{self.case['id']}/report")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json())
        self.assertEqual(self.client.get('/api/cases/999/report').status_code, 404)
        self.assertEqual(
            self.client.post('/api/cases/999/analysis-runs').status_code, 404,
        )
        self.assertEqual(
            self.client.get('/api/analysis-runs/999').status_code, 404,
        )

    def test_report_endpoint_returns_report_without_run_wrapper(self):
        run = self.run_analysis()
        response = self.client.get(f"/api/cases/{self.case['id']}/report")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json(), run['result'])
        self.assertNotIn('result', response.json())

    def test_reports_map_keeps_cases_separate_and_skips_failed_runs(self):
        other_case = self.create_case(title='Другая идея')
        run = self.run_analysis()
        self.db.add(AnalysisRun(
            case_id=self.case['id'],
            status=AnalysisStatus.FAILED.value,
            result=None,
        ))
        self.db.commit()
        response = self.client.get('/api/reports')
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json(), {
            str(self.case['id']): run['result'],
            str(other_case['id']): None,
        })

    def test_newest_completed_report_is_returned(self):
        self.run_analysis()
        self.client.patch(
            f"/api/cases/{self.case['id']}", json={'title': 'Обновлённая идея'},
        )
        newest_run = self.run_analysis()
        self.assertEqual(
            self.client.get(f"/api/cases/{self.case['id']}/report").json(),
            newest_run['result'],
        )

    def test_completed_run_with_json_null_does_not_hide_previous_report(self):
        previous = self.run_analysis()
        self.db.add(AnalysisRun(
            case_id=self.case['id'], status='completed', result=None,
        ))
        self.db.commit()
        self.assertEqual(
            self.client.get(f"/api/cases/{self.case['id']}/report").json(),
            previous['result'],
        )

    def test_analyzer_error_is_saved_as_failed(self):
        with patch(
            'app.api.analysis_runs.build_mock_report',
            side_effect=RuntimeError('Test analyzer error'),
        ):
            response = self.client.post(
                f"/api/cases/{self.case['id']}/analysis-runs",
            )
        self.assertEqual(response.status_code, 500)
        failed_run = self.db.query(AnalysisRun).one()
        stages = self.db.query(AnalysisStage).order_by(AnalysisStage.position).all()
        self.assertEqual(failed_run.status, 'failed')
        self.assertEqual(failed_run.error_message, 'Test analyzer error')
        self.assertEqual(stages[0].status, 'failed')
        self.assertTrue(all(stage.status == 'pending' for stage in stages[1:]))
        self.assertIsNone(
            self.client.get(f"/api/cases/{self.case['id']}/report").json(),
        )

    def test_reference_report_round_trips_through_http(self):
        reference = fixture('reports.json')['1']
        report = CaseReport.model_validate(reference)
        self.assertEqual(
            report.model_dump(mode='json', exclude_unset=True), reference,
        )
        self.db.add(AnalysisRun(
            case_id=self.case['id'],
            status='completed',
            result=reference,
        ))
        self.db.commit()
        response = self.client.get(f"/api/cases/{self.case['id']}/report")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(
            response.json(), report.model_dump(mode='json'),
        )

    def test_persisted_legacy_report_remains_readable(self):
        legacy = {
            'summary': 'Старое описание продукта',
            'target_audience': 'Студенты',
            'audience_segments': [{
                'name': 'Студенты', 'description': 'Сегмент', 'needs': ['Планирование'],
            }],
            'jtbd': [{
                'situation': 'Нет времени', 'motivation': 'Спланировать день',
                'expected_outcome': 'Успеть выполнить задачи',
            }],
            'risks': [{
                'description': 'Нет спроса', 'level': 'high', 'mitigation': 'Интервью',
            }],
            'recommendations': ['Проверить спрос'],
            'final_report_markdown': '# Старый отчёт',
        }
        run = AnalysisRun(case_id=self.case['id'], status='completed', result=legacy)
        self.db.add(run)
        self.db.commit()
        for url in (
            f"/api/cases/{self.case['id']}/report",
            f'/api/analysis-runs/{run.id}',
        ):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, response.text)
            data = response.json()
            payload = data.get('result', data)
            self.assertEqual(payload['overview']['idea'], legacy['summary'])
            self.assertEqual(payload['audience']['primarySegment'], 'Студенты')
            self.assertEqual(payload['risks']['items'][0]['cell'], 9)
            self.assertEqual(payload['markdown'], legacy['final_report_markdown'])
        self.db.refresh(run)
        self.assertEqual(run.result, legacy)
