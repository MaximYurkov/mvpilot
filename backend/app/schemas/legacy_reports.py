"""Read old persisted reports without deleting or rewriting their database rows."""

LEGACY_NOTE = (
    'Отчёт преобразован из прежнего формата. '
    'Новые оценки, расчёты и внешние источники отсутствуют.'
)


def upgrade_legacy_report(data: dict) -> dict:
    partial = {'status': 'partial', 'note': LEGACY_NOTE, 'sources': []}
    unavailable = {**partial, 'status': 'insufficient_data'}
    canvas = data.get('lean_canvas', {})
    recommendations = data.get('recommendations', [])
    return {
        'overview': {
            **partial, 'idea': data['summary'], 'readiness': [], 'tiles': [],
        },
        'market': {
            **unavailable,
            'tam': None, 'sam': None, 'som': None, 'method': None,
            'methodComment': None, 'assumptions': data.get('assumptions', []),
            'dynamics': [], 'dynamicsSource': None, 'trends': [],
        },
        'audience': {
            **partial,
            'primarySegment': data.get('target_audience'),
            'segments': [
                {**segment, 'estimatedShare': None}
                for segment in data.get('audience_segments', [])
            ],
            'jtbd': [
                {
                    'situation': item['situation'],
                    'motivation': item['motivation'],
                    'outcome': item['expected_outcome'],
                    'priority': 'medium',
                }
                for item in data.get('jtbd', [])
            ],
        },
        'competitors': {
            **unavailable,
            'axes': {'x': 'Полезность', 'y': 'Удобство'},
            'items': [], 'comparison': [],
            'swot': {
                'strengths': [], 'weaknesses': [], 'opportunities': [], 'threats': [],
            },
        },
        'leanCanvas': {
            **partial,
            'problems': canvas.get('problems', []),
            'solutions': canvas.get('solutions', []),
            'value': canvas.get('unique_value_proposition', ''),
            'advantage': canvas.get('unfair_advantage', ''),
            'segments': canvas.get('customer_segments', []),
            'metrics': canvas.get('key_metrics', []),
            'channels': canvas.get('channels', []),
            'costs': canvas.get('cost_structure', []),
            'revenue': canvas.get('revenue_streams', []),
        },
        'mvp': {**partial, 'features': data.get('mvp', []), 'userFlow': []},
        'roadmap': {**unavailable, 'stages': []},
        'metrics': {
            **unavailable,
            'northStar': {'name': 'Главная метрика ещё не определена', 'value': None, 'unit': ''},
            'tree': None, 'funnel': [],
        },
        'finance': {
            **unavailable, 'figures': [], 'recommendedTotal': None, 'budgetSections': [],
        },
        'risks': {
            **partial,
            'note': LEGACY_NOTE + ' Старые уровни low/medium/high показаны в клетках 1/5/9.',
            'items': [
                {
                    'cell': {'low': 1, 'medium': 5, 'high': 9}[risk['level']],
                    'description': risk['description'],
                    'mitigation': risk['mitigation'],
                    'cheapCheck': 'Способ проверки нужно уточнить.',
                }
                for risk in data.get('risks', [])
            ],
        },
        'nextSteps': {
            **partial,
            'items': [
                {
                    'title': item, 'description': item,
                    'priority': 'should', 'effort': 'medium', 'partner': None,
                }
                for item in recommendations
            ],
        },
        'markdown': data['final_report_markdown'],
    }
