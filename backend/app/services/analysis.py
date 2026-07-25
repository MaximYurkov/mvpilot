from app.core.cases import CaseStage
from app.db.models import Case
from app.schemas.analysis_runs import (
    AnalysisReport,
    AudienceSegment,
    BacklogItem,
    BacklogPriority,
    CriticReview,
    JTBDItem,
    LeanCanvas,
    MVPFeature,
    ProductRisk,
    RiskLevel,
    RoadmapStage,
)

CASE_STAGE_LABELS = {
    CaseStage.IDEA.value: 'идея',
    CaseStage.VALIDATION.value: 'проверка гипотез',
    CaseStage.PROTOTYPE.value: 'прототип',
    CaseStage.MVP.value: 'MVP',
    CaseStage.LAUNCHED.value: 'запущенный продукт',
}


def build_mock_report(case: Case) -> AnalysisReport:
    audience = case.audience or 'Первый узкий сегмент пользователей ещё не определён.'
    problem = case.problem or 'Проблема пользователя требует уточнения.'
    stage = CASE_STAGE_LABELS.get(case.stage, case.stage)
    analysis_goal = (
        case.analysis_goal
        or 'Получить структурированный черновик продуктового кейса.'
    )
    value_proposition = (
        f'{case.title} помогает аудитории «{audience}» решить следующую проблему: '
        f'{problem.lower()}'
    )

    assumptions = [
        'Описание аудитории и её потребностей пока является гипотезой.',
        'Рыночные выводы не подтверждены внешними источниками.',
        'Состав MVP нужно проверить интервью и прототипом.',
        f'Текущая стадия проекта указана как «{stage}».',
    ]
    analysis_plan = [
        f'Учесть цель анализа: {analysis_goal}',
        'Уточнить проблему и сегменты целевой аудитории.',
        'Проверить ценностное предложение и сформулировать JTBD.',
        'Определить Lean Canvas, состав MVP и продуктовые метрики.',
        'Составить первый backlog, roadmap и список рисков.',
        'Проверить согласованность продуктового кейса.',
    ]
    audience_segments = [
        AudienceSegment(
            name=audience,
            description='Предполагаемый первый сегмент пользователей продукта.',
            needs=[
                f'Решить проблему: {problem}',
                'Получить понятный результат без лишней сложности.',
            ],
        )
    ]
    jtbd = [
        JTBDItem(
            situation=f'пользователь сталкивается с проблемой «{problem}»',
            motivation=f'воспользоваться продуктом «{case.title}»',
            expected_outcome='чтобы быстрее получить полезный и понятный результат',
        )
    ]
    lean_canvas = LeanCanvas(
        problems=[
            problem,
            'Существующий способ решения может занимать много времени.',
        ],
        customer_segments=[audience],
        unique_value_proposition=value_proposition,
        solutions=[
            'Простой основной сценарий решения пользовательской проблемы.',
            'Сохранение результата для дальнейшей работы.',
        ],
        channels=[
            'Тематические сообщества.',
            'Учебные проекты и рекомендации первых пользователей.',
        ],
        revenue_streams=[
            'Гипотеза: бесплатная базовая версия и платные расширенные возможности.',
        ],
        cost_structure=[
            'Разработка и поддержка приложения.',
            'Инфраструктура и используемые внешние сервисы.',
        ],
        key_metrics=[
            'Количество пользователей, завершивших основной сценарий.',
            'Доля пользователей, которые возвращаются к продукту.',
        ],
        unfair_advantage=(
            'Гипотеза: более простой и сфокусированный сценарий для выбранной аудитории.'
        ),
    )
    mvp = [
        MVPFeature(
            name='Создание проекта',
            description='Пользователь сохраняет исходные данные своей идеи.',
            priority=BacklogPriority.MUST,
        ),
        MVPFeature(
            name='Основной полезный сценарий',
            description=f'Продукт помогает решить проблему: {problem}',
            priority=BacklogPriority.MUST,
        ),
        MVPFeature(
            name='Просмотр результата',
            description='Пользователь видит и может повторно открыть результат работы.',
            priority=BacklogPriority.SHOULD,
        ),
    ]
    backlog = [
        BacklogItem(
            epic='Управление проектом',
            user_story=(
                'Как пользователь, я хочу создать проект, '
                'чтобы сохранить исходную информацию.'
            ),
            acceptance_criteria=[
                'Пользователь может заполнить обязательные поля.',
                'После сохранения проект доступен для просмотра.',
            ],
            priority=BacklogPriority.MUST,
        ),
        BacklogItem(
            epic='Основной сценарий',
            user_story=(
                'Как пользователь, я хочу пройти основной сценарий продукта, '
                'чтобы получить ожидаемую ценность.'
            ),
            acceptance_criteria=[
                'Сценарий можно запустить для существующего проекта.',
                'Результат сценария сохраняется.',
                'Ошибка отображается в понятном виде.',
            ],
            priority=BacklogPriority.MUST,
        ),
    ]
    roadmap = [
        RoadmapStage(
            name='Проверка гипотез',
            goal='Понять, существует ли проблема у выбранной аудитории.',
            deliverables=[
                'Интервью с потенциальными пользователями.',
                'Уточнённые проблема и ценностное предложение.',
            ],
        ),
        RoadmapStage(
            name='MVP',
            goal='Проверить основной полезный сценарий.',
            deliverables=[
                'Рабочий прототип.',
                'Сбор обратной связи и основных метрик.',
            ],
        ),
        RoadmapStage(
            name='Первая версия',
            goal='Улучшить продукт на основе результатов MVP.',
            deliverables=[
                'Исправления основных проблем.',
                'Функции с подтверждённым пользовательским спросом.',
            ],
        ),
    ]
    risks = [
        ProductRisk(
            description='Проблема может быть недостаточно значимой для аудитории.',
            level=RiskLevel.HIGH,
            mitigation='Провести интервью до разработки полного продукта.',
        ),
        ProductRisk(
            description='Состав MVP может оказаться слишком большим.',
            level=RiskLevel.MEDIUM,
            mitigation='Оставить только функции основного пользовательского сценария.',
        ),
        ProductRisk(
            description='Рыночные предположения пока не подтверждены.',
            level=RiskLevel.MEDIUM,
            mitigation='Проверить конкурентов и альтернативные способы решения проблемы.',
        ),
    ]
    critic_issues = [
        'Пока нет результатов интервью с представителями аудитории.',
        'Ключевые метрики требуют числовых целевых значений.',
    ]

    if case.audience is None:
        critic_issues.append('Не указан конкретный сегмент целевой аудитории.')
        risks.append(
            ProductRisk(
                description='Слишком широкая или неизвестная целевая аудитория.',
                level=RiskLevel.HIGH,
                mitigation='Выбрать один первый сегмент для проверки гипотезы.',
            )
        )

    if case.problem is None:
        critic_issues.append('Пользовательская проблема явно не сформулирована.')
        risks.append(
            ProductRisk(
                description='Функции продукта могут не решать реальную проблему.',
                level=RiskLevel.HIGH,
                mitigation='Сформулировать и проверить проблему до разработки MVP.',
            )
        )

    recommendations = [
        'Провести 5–7 интервью с представителями первого сегмента.',
        'Проверить ключевую гипотезу небольшим прототипом.',
        'Определить одну главную метрику успеха MVP.',
    ]
    critic_review = CriticReview(
        issues=critic_issues,
        contradictions=[],
        recommendations=recommendations,
    )
    final_report_markdown = _build_mock_markdown(
        case=case,
        stage=stage,
        analysis_goal=analysis_goal,
        audience=audience,
        problem=problem,
        value_proposition=value_proposition,
        jtbd=jtbd,
        lean_canvas=lean_canvas,
        mvp=mvp,
        backlog=backlog,
        roadmap=roadmap,
        risks=risks,
        critic_review=critic_review,
        recommendations=recommendations,
    )

    return AnalysisReport(
        summary=(
            f'«{case.title}» — продукт на стадии «{stage}»: {case.description}'
        ),
        analysis_plan=analysis_plan,
        assumptions=assumptions,
        problem=problem,
        target_audience=audience,
        audience_segments=audience_segments,
        value_proposition=value_proposition,
        jtbd=jtbd,
        lean_canvas=lean_canvas,
        mvp=mvp,
        backlog=backlog,
        roadmap=roadmap,
        risks=risks,
        critic_review=critic_review,
        recommendations=recommendations,
        final_report_markdown=final_report_markdown,
    )


def _build_mock_markdown(
    *,
    case: Case,
    stage: str,
    analysis_goal: str,
    audience: str,
    problem: str,
    value_proposition: str,
    jtbd: list[JTBDItem],
    lean_canvas: LeanCanvas,
    mvp: list[MVPFeature],
    backlog: list[BacklogItem],
    roadmap: list[RoadmapStage],
    risks: list[ProductRisk],
    critic_review: CriticReview,
    recommendations: list[str],
) -> str:
    canvas_problems = '\n'.join(f'- {item}' for item in lean_canvas.problems)
    canvas_solutions = '\n'.join(f'- {item}' for item in lean_canvas.solutions)
    mvp_text = '\n'.join(f'- {feature.name}: {feature.description}' for feature in mvp)
    backlog_text = '\n'.join(f'- {item.user_story}' for item in backlog)
    roadmap_text = '\n'.join(f'- {stage.name}: {stage.goal}' for stage in roadmap)
    risks_text = '\n'.join(f'- {risk.description}' for risk in risks)
    critic_text = '\n'.join(f'- {issue}' for issue in critic_review.issues)
    recommendations_text = '\n'.join(f'- {item}' for item in recommendations)
    first_jtbd = jtbd[0]

    return f"""# {case.title}

## Описание

{case.description}

Текущая стадия: {stage}

Цель анализа: {analysis_goal}

## Проблема

{problem}

## Целевая аудитория

{audience}

## Ценностное предложение

{value_proposition}

## JTBD

Когда {first_jtbd.situation.lower()}, я хочу {first_jtbd.motivation.lower()},
{first_jtbd.expected_outcome.lower()}.

## Lean Canvas

Проблемы:

{canvas_problems}

Решения:

{canvas_solutions}

Уникальное ценностное предложение: {lean_canvas.unique_value_proposition}

## MVP

{mvp_text}

## Backlog

{backlog_text}

## Roadmap

{roadmap_text}

## Риски

{risks_text}

## Критика

{critic_text}

## Рекомендации

{recommendations_text}

> Отчёт создан mock-анализом. Все продуктовые выводы требуют проверки.
"""
