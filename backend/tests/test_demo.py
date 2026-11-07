from app.db.models import AnalysisRun, Case
from scripts.seed_demo import seed_demo
from tests.support import APITestCase, fixture


class DemoTestCase(APITestCase):
    def test_demo_cases_match_reference_and_reports_keep_null(self):
        seed_demo(self.db)
        expected = sorted(fixture('cases.json'), key=lambda item: item['id'])
        response = self.client.get('/api/cases')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(sorted(response.json(), key=lambda item: item['id']), expected)
        reports = self.client.get('/api/reports')
        self.assertEqual(reports.status_code, 200)
        self.assertIsNone(reports.json()['2'])
        self.assertEqual(
            reports.json()['1']['overview'], fixture('reports.json')['1']['overview'],
        )

    def test_demo_does_not_overwrite_existing_data(self):
        self.create_case()
        with self.assertRaises(ValueError):
            seed_demo(self.db)
        self.assertEqual(self.db.query(Case).count(), 1)
        self.assertEqual(self.db.query(AnalysisRun).count(), 0)
