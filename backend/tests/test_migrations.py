import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from sqlalchemy import create_engine, inspect

BACKEND_DIR = Path(__file__).resolve().parents[1]


class MigrationsTestCase(unittest.TestCase):
    def test_upgrade_check_and_downgrade(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / 'migration_test.db'
            database_url = f'sqlite:///{database_path.as_posix()}'
            environment = {
                **os.environ,
                'MVPILOT_DATABASE_URL': database_url,
            }

            self.run_alembic('upgrade', 'head', environment=environment)

            engine = create_engine(database_url)
            inspector = inspect(engine)

            self.assertEqual(
                set(inspector.get_table_names()),
                {
                    'alembic_version',
                    'analysis_runs',
                    'analysis_stages',
                    'cases',
                },
            )
            self.assertEqual(
                {column['name'] for column in inspector.get_columns('cases')},
                {
                    'id',
                    'title',
                    'description',
                    'audience',
                    'problem',
                    'stage',
                    'analysis_goal',
                    'created_at',
                    'updated_at',
                },
            )
            self.assertEqual(
                {column['name'] for column in inspector.get_columns('analysis_runs')},
                {
                    'id',
                    'case_id',
                    'status',
                    'result',
                    'error_message',
                    'started_at',
                    'finished_at',
                },
            )
            self.assertEqual(
                {
                    column['name']
                    for column in inspector.get_columns('analysis_stages')
                },
                {
                    'id',
                    'analysis_run_id',
                    'name',
                    'position',
                    'status',
                    'result',
                    'error_message',
                    'started_at',
                    'finished_at',
                },
            )
            self.assertEqual(
                inspector.get_foreign_keys('analysis_stages')[0][
                    'referred_table'
                ],
                'analysis_runs',
            )
            engine.dispose()

            self.run_alembic('check', environment=environment)
            self.run_alembic('downgrade', 'base', environment=environment)

            downgraded_engine = create_engine(database_url)
            downgraded_tables = set(inspect(downgraded_engine).get_table_names())
            downgraded_engine.dispose()

            self.assertNotIn('cases', downgraded_tables)
            self.assertNotIn('analysis_runs', downgraded_tables)
            self.assertNotIn('analysis_stages', downgraded_tables)

    def run_alembic(self, *arguments: str, environment: dict[str, str]) -> None:
        result = subprocess.run(
            [sys.executable, '-m', 'alembic', *arguments],
            cwd=BACKEND_DIR,
            env=environment,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            self.fail(
                f'Alembic command failed: {" ".join(arguments)}\n'
                f'{result.stdout}\n{result.stderr}'
            )


if __name__ == '__main__':
    unittest.main()
