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

    def test_report_routes_publish_the_frontend_contract(self):
        schemas = app.openapi()['components']['schemas']
        report = schemas['CaseReport']
        self.assertEqual(set(report['properties']), {
            'overview', 'market', 'audience', 'competitors', 'leanCanvas',
            'mvp', 'roadmap', 'metrics', 'finance', 'risks', 'nextSteps',
            'markdown',
        })
        self.assertEqual(set(report['required']), set(report['properties']))
        self.assertEqual(set(schemas['Case']['properties']), {
            'id', 'title', 'description', 'audience', 'createdAt', 'updatedAt',
        })
        self.assertEqual(set(schemas['CaseFormValues']['required']), {
            'title', 'description', 'audience',
        })
        self.assertEqual(set(schemas['Priority']['enum']), {
            'must', 'should', 'could', 'wont',
        })
        self.assertIn('getCaseReport', [
            operation['operationId']
            for item in app.openapi()['paths'].values()
            for operation in item.values()
        ])

    def test_nullable_is_different_from_optional(self):
        schemas = app.openapi()['components']['schemas']
        self.assertIn('tam', schemas['Market']['required'])
        self.assertIn({'type': 'null'}, schemas['Market']['properties']['tam']['anyOf'])
        node = schemas.get('MetricNode', schemas.get('MetricNode-Output'))
        self.assertNotIn('children', node['required'])
        self.assertEqual(node['properties']['children']['type'], 'array')


if __name__ == '__main__':
    unittest.main()
