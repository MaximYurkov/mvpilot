from app.core.analysis import AnalysisStageName
from app.db.models import Case
from app.schemas.reports import CaseReport

MOCK_NOTE = (
    'Локальный mock-черновик без LLM и внешних источников. '
    'Продуктовые гипотезы требуют проверки.'
)
NO_DATA_NOTE = (
    'Нет подтверждённых данных. Числа и источники не подставлены автоматически.'
)


def build_mock_report(case: Case) -> CaseReport:
    audience = case.audience or 'Целевая аудитория ещё не определена'
    problem = case.problem or 'Пользовательскую проблему нужно уточнить интервью.'
    north_star = 'Пользователи, завершившие основной полезный сценарий'
    partial = {'status': 'partial', 'note': MOCK_NOTE, 'sources': []}
    unavailable = {
        'status': 'insufficient_data',
        'note': NO_DATA_NOTE,
        'sources': [],
    }

    return CaseReport.model_validate({
        'overview': {
            **partial,
            'idea': f'{case.title}: {case.description}',
            'readiness': [],
            'tiles': [],
        },
        'market': {
            **unavailable,
            'tam': None,
            'sam': None,
            'som': None,
            'method': None,
            'methodComment': None,
            'assumptions': [],
            'dynamics': [],
            'dynamicsSource': None,
            'trends': [],
        },
        'audience': {
            **partial,
            'primarySegment': case.audience or None,
            'segments': [{
                'name': audience,
                'estimatedShare': None,
                'description': 'Первый предполагаемый сегмент из описания кейса.',
                'needs': [problem],
            }],
            'jtbd': [{
                'situation': f'когда возникает потребность в продукте «{case.title}»',
                'motivation': 'я хочу пройти основной сценарий без лишних действий',
                'outcome': 'чтобы получить полезный результат',
                'priority': 'high',
            }],
        },
        'competitors': {
            **unavailable,
            'axes': {'x': 'Полезность', 'y': 'Удобство'},
            'items': [{
                'name': case.title,
                'x': None,
                'y': None,
                'isProduct': True,
                'url': None,
                'strengths': [],
                'weaknesses': [],
            }],
            'comparison': [],
            'swot': {
                'strengths': [],
                'weaknesses': ['Нет подтверждения пользовательского спроса.'],
                'opportunities': [],
                'threats': ['Пользователи могут предпочесть существующие альтернативы.'],
            },
        },
        'leanCanvas': {
            **partial,
            'problems': [problem],
            'solutions': [case.description],
            'value': f'Помочь аудитории «{audience}» получить основной результат.',
            'advantage': 'Отличие от альтернатив ещё нужно подтвердить.',
            'segments': [audience],
            'metrics': [north_star],
            'channels': ['Проверить спрос в сообществах целевой аудитории.'],
            'costs': ['Оценить стоимость разработки и поддержки.'],
            'revenue': ['Проверить готовность аудитории платить.'],
        },
        'mvp': {
            **partial,
            'features': [
                {
                    'name': 'Основной полезный сценарий',
                    'description': case.description,
                    'priority': 'must',
                },
                {
                    'name': 'Просмотр результата',
                    'description': 'Повторно открыть полученный результат.',
                    'priority': 'should',
                },
                {
                    'name': 'Дополнительные сценарии',
                    'description': 'Отложить до проверки основного спроса.',
                    'priority': 'wont',
                },
            ],
            'userFlow': [
                {'step': 'Открыть продукт', 'description': 'Понять предлагаемую ценность.'},
                {'step': 'Ввести данные', 'description': 'Передать данные для основного сценария.'},
                {'step': 'Получить результат', 'description': 'Оценить полезность решения.'},
            ],
        },
        'roadmap': {**unavailable, 'stages': []},
        'metrics': {
            **partial,
            'northStar': {'name': north_star, 'value': None, 'unit': 'в месяц'},
            'tree': {
                'name': north_star,
                'children': [
                    {'name': 'Привлечение целевой аудитории'},
                    {'name': 'Конверсия в полезный результат'},
                    {'name': 'Повторное использование'},
                ],
            },
            'funnel': [],
        },
        'finance': {
            **unavailable,
            'figures': [],
            'recommendedTotal': None,
            'budgetSections': [],
        },
        'risks': {
            **partial,
            'items': [
                {
                    'cell': 9,
                    'description': 'Проблема может быть недостаточно важна для аудитории.',
                    'mitigation': 'Проверить проблему до разработки полной версии.',
                    'cheapCheck': 'Провести 5–7 интервью.',
                },
                {
                    'cell': 6,
                    'description': 'Состав MVP может оказаться слишком большим.',
                    'mitigation': 'Оставить один основной пользовательский сценарий.',
                    'cheapCheck': 'Показать прототип представителям аудитории.',
                },
                {
                    'cell': 5,
                    'description': 'Экономика продукта ещё не подтверждена.',
                    'mitigation': 'Собрать оценки расходов и спроса.',
                    'cheapCheck': 'Получить предложения подрядчиков и проверить цену.',
                },
            ],
        },
        'nextSteps': {
            **partial,
            'items': [
                {
                    'title': 'Провести интервью',
                    'description': f'Проверить проблему сегмента «{audience}».',
                    'priority': 'must',
                    'effort': 'medium',
                    'partner': None,
                },
                {
                    'title': 'Проверить основной сценарий',
                    'description': 'Собрать небольшой прототип и показать пользователям.',
                    'priority': 'must',
                    'effort': 'medium',
                    'partner': None,
                },
                {
                    'title': 'Собрать данные для расчётов',
                    'description': 'Найти источники рынка и получить оценки расходов.',
                    'priority': 'should',
                    'effort': 'high',
                    'partner': None,
                },
            ],
        },
        'markdown': (
            f'# {case.title}\n\n'
            f'## Обзор\n\n{case.description}\n\n'
            f'## Аудитория\n\n{audience}\n\n'
            f'## Проблема\n\n{problem}\n\n'
            '## Lean Canvas\n\nПроверить сегмент, ценность и способ монетизации.\n\n'
            '## MVP\n\nОдин основной пользовательский сценарий и просмотр результата.\n\n'
            '## Рынок, конкуренты и финансы\n\nНет подтверждённых данных.\n\n'
            '## Метрики\n\nОпределить конверсию в полезный результат.\n\n'
            '## Следующие шаги\n\nПровести интервью и проверить прототип.\n\n'
            f'> {MOCK_NOTE}\n'
        ),
    })


def build_mock_stage_results(
    report: CaseReport,
) -> dict[AnalysisStageName, dict[str, object]]:
    payload = report.model_dump(mode='json')
    return {
        AnalysisStageName.PLANNER: {
            'sections': [name for name in payload if name != 'markdown'],
            'note': MOCK_NOTE,
        },
        AnalysisStageName.MARKET_ANALYST: {
            name: payload[name] for name in ('market', 'audience', 'competitors')
        },
        AnalysisStageName.PRODUCT_MANAGER: {
            name: payload[name]
            for name in ('leanCanvas', 'mvp', 'roadmap', 'metrics', 'finance')
        },
        AnalysisStageName.CRITIC: {
            name: payload[name] for name in ('risks', 'nextSteps')
        },
        AnalysisStageName.EDITOR: {
            name: payload[name] for name in ('overview', 'markdown')
        },
    }
