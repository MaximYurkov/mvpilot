from app.db.models import Case
from app.schemas.analysis_runs import AnalysisReport


def build_mock_report(case: Case) -> AnalysisReport:
    target_audience = case.audience or 'Целевая аудитория пока не указана.'
    problem = case.problem or 'Проблема пользователя пока не сформулирована.'

    risks = [
        'Выводы ещё не подтверждены интервью с потенциальными пользователями.',
        'Не определены измеримые критерии успеха продукта.',
    ]
    recommendations = [
        'Провести несколько интервью с представителями целевой аудитории.',
        'Сформулировать одну главную метрику для первой версии продукта.',
        'Проверить ключевую гипотезу с помощью небольшого прототипа.',
    ]

    if case.audience is None:
        risks.append('Без описания аудитории сложно проверить востребованность идеи.')
        recommendations.append('Описать первый узкий сегмент целевой аудитории.')

    if case.problem is None:
        risks.append('Без явной проблемы ценность продукта остаётся неясной.')
        recommendations.append('Сформулировать проблему, которую решает продукт.')

    return AnalysisReport(
        summary=(
            f'«{case.title}» — продуктовая идея со следующим описанием: '
            f'{case.description}'
        ),
        target_audience=target_audience,
        problem=problem,
        strengths=[
            'У идеи есть название и описание.',
            'Кейс сохранён в едином формате и готов к дальнейшему анализу.',
        ],
        risks=risks,
        recommendations=recommendations,
    )
