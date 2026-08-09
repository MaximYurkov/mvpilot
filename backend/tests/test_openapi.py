import json
import unittest
from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware

from app.main import app, default_cors_origins


class OpenAPITestCase(unittest.TestCase):
    def test_saved_specification_is_current(self):
        specification_path = Path(__file__).parents[1] / 'openapi.json'
        saved_specification = json.loads(
            specification_path.read_text(encoding='utf-8')
        )

        self.assertEqual(saved_specification, app.openapi())

    def test_operation_ids_are_unique_and_readable(self):
        operation_ids = [
            operation['operationId']
            for path in app.openapi()['paths'].values()
            for operation in path.values()
        ]

        self.assertEqual(len(operation_ids), len(set(operation_ids)))
        self.assertIn('createCase', operation_ids)
        self.assertIn('createAnalysisRun', operation_ids)
        self.assertIn('getAnalysisRun', operation_ids)

    def test_error_responses_are_documented(self):
        paths = app.openapi()['paths']
        expected_error_statuses = {
            ('/api/cases', 'get'): {'500'},
            ('/api/cases', 'post'): {'422', '500'},
            ('/api/cases/{case_id}', 'get'): {'404', '422', '500'},
            ('/api/cases/{case_id}', 'patch'): {'404', '422', '500'},
            ('/api/cases/{case_id}', 'delete'): {'404', '422', '500'},
            ('/api/cases/{case_id}/analysis-runs', 'post'): {
                '404',
                '422',
                '500',
            },
            ('/api/cases/{case_id}/analysis-runs', 'get'): {
                '404',
                '422',
                '500',
            },
            ('/api/analysis-runs/{run_id}', 'get'): {
                '404',
                '422',
                '500',
            },
        }

        for (path, method), expected_statuses in expected_error_statuses.items():
            responses = paths[path][method]['responses']
            self.assertTrue(expected_statuses.issubset(responses))

            for status_code in expected_statuses - {'422'}:
                error_schema = responses[status_code]['content'][
                    'application/json'
                ]['schema']
                self.assertEqual(
                    error_schema['$ref'],
                    '#/components/schemas/ErrorResponse',
                )

    def test_local_frontend_origins_are_allowed(self):
        cors_middleware = next(
            middleware
            for middleware in app.user_middleware
            if middleware.cls is CORSMiddleware
        )

        self.assertEqual(
            cors_middleware.kwargs['allow_origins'],
            list(default_cors_origins),
        )


if __name__ == '__main__':
    unittest.main()
