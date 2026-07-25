import unittest

from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.cases import create_case, get_case, get_cases, update_case
from app.core.cases import CaseStage
from app.db.base import Base
from app.schemas.cases import CaseCreate, CaseRead, CaseUpdate


class CasesTestCase(unittest.TestCase):
    def setUp(self):
        engine = create_engine(
            'sqlite://',
            connect_args={'check_same_thread': False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(bind=engine)
        self.engine = engine
        self.db = sessionmaker(bind=engine)()

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def test_create_case_uses_idea_as_default_stage(self):
        case = create_case(
            CaseCreate(
                title='Новая идея',
                description='Описание продуктовой идеи.',
            ),
            self.db,
        )
        response = CaseRead.model_validate(case)

        self.assertEqual(response.stage, CaseStage.IDEA)
        self.assertIsNone(response.analysis_goal)

    def test_stage_and_analysis_goal_can_be_created_read_and_updated(self):
        case = create_case(
            CaseCreate(
                title='Учебный планировщик',
                description='Помогает студентам планировать задачи.',
                stage=CaseStage.PROTOTYPE,
                analysis_goal='Проверить состав MVP',
            ),
            self.db,
        )

        fetched_case = get_case(case.id, self.db)
        updated_case = update_case(
            case.id,
            CaseUpdate(
                stage=CaseStage.MVP,
                analysis_goal='Подготовить roadmap первой версии',
            ),
            self.db,
        )
        cases = get_cases(self.db)

        self.assertEqual(fetched_case.id, case.id)
        self.assertEqual(updated_case.stage, CaseStage.MVP.value)
        self.assertEqual(
            updated_case.analysis_goal,
            'Подготовить roadmap первой версии',
        )
        self.assertEqual([item.id for item in cases], [case.id])

    def test_unknown_stage_is_rejected(self):
        with self.assertRaises(ValidationError):
            CaseCreate(
                title='Новая идея',
                description='Описание.',
                stage='unknown',
            )

    def test_required_update_fields_cannot_be_null(self):
        with self.assertRaises(ValidationError):
            CaseUpdate(stage=None)


if __name__ == '__main__':
    unittest.main()
