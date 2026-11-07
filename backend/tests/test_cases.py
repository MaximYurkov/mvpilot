from app.db.models import AnalysisRun, AnalysisStage, Case
from tests.support import APITestCase, fixture


class CasesTestCase(APITestCase):
    def test_create_and_read_use_exact_frontend_shape(self):
        case = self.create_case()
        expected_keys = {
            'id', 'title', 'description', 'audience', 'createdAt', 'updatedAt',
        }
        self.assertEqual(set(case), expected_keys)
        self.assertIsInstance(case['id'], int)
        self.assertEqual(
            self.client.get(f"/api/cases/{case['id']}").json(),
            case,
        )
        self.assertEqual(self.client.get('/api/cases').json(), [case])

    def test_fixture_fields_can_be_created(self):
        for example in fixture('cases.json'):
            self.create_case(**{
                key: example[key] for key in ('title', 'description', 'audience')
            })

    def test_missing_or_blank_form_fields_are_rejected(self):
        for field in ('title', 'description', 'audience'):
            for value in (None, '', '   '):
                with self.subTest(field=field, value=value):
                    data = {
                        'title': 'Идея',
                        'description': 'Описание',
                        'audience': 'Студенты',
                        field: value,
                    }
                    self.assertEqual(
                        self.client.post('/api/cases', json=data).status_code, 422,
                    )

    def test_old_context_fields_are_not_silently_accepted(self):
        response = self.client.post('/api/cases', json={
            'title': 'Идея',
            'description': 'Описание',
            'audience': 'Студенты',
            'stage': 'prototype',
        })
        self.assertEqual(response.status_code, 422)

    def test_patch_changes_only_supplied_fields(self):
        case = self.create_case()
        response = self.client.patch(
            f"/api/cases/{case['id']}", json={'title': 'Новое название'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Новое название')
        self.assertEqual(response.json()['audience'], case['audience'])
        self.assertEqual(response.json()['createdAt'], case['createdAt'])

    def test_patch_rejects_explicit_null(self):
        case = self.create_case()
        for field in ('title', 'description', 'audience'):
            self.assertEqual(
                self.client.patch(
                    f"/api/cases/{case['id']}", json={field: None},
                ).status_code,
                422,
            )

    def test_legacy_nullable_audience_is_serialized_as_string(self):
        case = Case(title='Старая идея', description='Описание', audience=None)
        self.db.add(case)
        self.db.commit()
        response = self.client.get(f'/api/cases/{case.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['audience'], '')
        self.assertNotIn('problem', response.json())
        self.assertNotIn('stage', response.json())

    def test_delete_removes_dependent_runs_and_stages(self):
        case = self.create_case()
        self.assertEqual(
            self.client.post(
                f"/api/cases/{case['id']}/analysis-runs",
            ).status_code,
            201,
        )
        response = self.client.delete(f"/api/cases/{case['id']}")
        self.assertEqual(response.status_code, 204, response.text)
        self.assertEqual(response.content, b'')
        self.assertEqual(self.db.query(AnalysisRun).count(), 0)
        self.assertEqual(self.db.query(AnalysisStage).count(), 0)
        self.assertEqual(self.client.get('/api/cases').json(), [])

    def test_unknown_case_returns_documented_404(self):
        self.assertEqual(
            self.client.get('/api/cases/999').json(),
            {'detail': 'Case not found'},
        )
        self.assertEqual(self.client.delete('/api/cases/999').status_code, 404)

    def test_cors_allows_local_frontend(self):
        response = self.client.options('/api/cases', headers={
            'Origin': 'http://localhost:5173',
            'Access-Control-Request-Method': 'POST',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers['access-control-allow-origin'],
            'http://localhost:5173',
        )
