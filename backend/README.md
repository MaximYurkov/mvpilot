# MVPilot Backend

FastAPI + SQLAlchemy + SQLite. Backend возвращает данные по текущему frontend-контракту:
`Case`, `CaseFormValues` и `CaseReport`.

## Локальный запуск

Из папки `backend`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Для запуска без тестов достаточно `requirements.txt`.
API: http://127.0.0.1:8000/api/health, Swagger: http://127.0.0.1:8000/docs.

База по умолчанию — `mvpilot.db` в текущей папке. Другую базу можно задать через
`MVPILOT_DATABASE_URL`. Миграции применяются явно, импорт приложения базу не создаёт.

## Контракт frontend

Эталон — собственные доменные типы frontend в
`src/entities/case/model/types.ts`, `src/entities/report/model/types.ts`
и примеры `public/cases.json`, `public/reports.json`.

JSON-ответ кейса содержит ровно:

```json
{
  "id": 1,
  "title": "Название",
  "description": "Описание",
  "audience": "Аудитория",
  "createdAt": "2026-09-15T10:00:00",
  "updatedAt": "2026-09-20T14:30:00"
}
```

Создание принимает три обязательных поля: `title`, `description`, `audience`.
Пробельные значения, неизвестные поля и явный `null` отклоняются.
Лимиты совпадают с формой: 50 символов для названия, 200 для описания и аудитории.
`PATCH` принимает любое подмножество этих трёх полей.

Старые поля контекста `problem`, `stage`, `analysis_goal` остаются в БД для сохранности
данных, но больше не входят в публичную модель кейса и не принимаются формой.
Для старых записей с `audience = NULL` в ответе используется пустая строка.

`CaseReport` содержит 11 фиксированных разделов: `overview`, `market`, `audience`,
`competitors`, `leanCanvas`, `mvp`, `roadmap`, `metrics`, `finance`, `risks`,
`nextSteps`, а также `markdown`.

Каждый раздел включает `status`, `note`, `sources`.
Статусы: `ready`, `partial`, `insufficient_data`, `not_applicable`.
Nullable-поля обязательны и явно возвращают `null`, когда значение неизвестно.
Необязательный массив `MetricNode.children` при отсутствии сериализуется как `[]`.
Сохранены текущие `competitor1/2/3` и `Risk.cell` от 1 до 9.

Эталонные JSON-снимки для тестов находятся в `tests/fixtures`. В них устранены
два расхождения с TypeScript: даты приведены к `createdAt/updatedAt`,
отсутствующий `partner.url` заполнен `null`. Исходный frontend не менялся.

## Маршруты

| Метод  | Путь                                 | Ответ                                     |
| ------ | ------------------------------------ | ----------------------------------------- | ------ |
| GET    | `/api/cases`                         | `Case[]`                                  |
| POST   | `/api/cases`                         | созданный `Case`, HTTP 201                |
| GET    | `/api/cases/{case_id}`               | `Case`                                    |
| PATCH  | `/api/cases/{case_id}`               | обновлённый `Case`                        |
| DELETE | `/api/cases/{case_id}`               | HTTP 204, удаляет также запуски и этапы   |
| POST   | `/api/cases/{case_id}/analysis-runs` | `AnalysisRunRead`, HTTP 201               |
| GET    | `/api/cases/{case_id}/analysis-runs` | история запусков                          |
| GET    | `/api/analysis-runs/{run_id}`        | запуск с `result: CaseReport              | null`  |
| GET    | `/api/cases/{case_id}/report`        | последний завершённый `CaseReport         | null`  |
| GET    | `/api/reports`                       | словарь по ID: `Record<string, CaseReport | null>` |

Существующий кейс без завершённого анализа возвращает HTTP 200 + `null`.
Неизвестный кейс — HTTP 404 + `{"detail": "Case not found"}`.
После неудачного повторного анализа доступен предыдущий завершённый отчёт.

## Анализ и старые отчёты

Анализ пока выполняется локальной mock-функцией, без LLM и LangGraph.
Она использует название, описание и аудиторию конкретного кейса, создаёт черновик
с пятью этапами и сохраняет новый формат отчёта в SQLite.
POST выполняет анализ синхронно; фонового выполнения и реального прогресса пока нет.

Непроверенные продуктовые предположения помечаются `partial`.
Без подтверждённых чисел рынок, бюджет и временные оценки остаются
`insufficient_data`: используются `null` и пустые массивы.
Готовый результат задачи не означает, что каждый раздел отчёта имеет статус `ready`.

Сохранённые отчёты прежнего формата преобразуются при чтении:
известные тексты переносятся в новые разделы, отсутствующие расчёты не придумываются.
Исходный JSON в базе не перезаписывается. Старые уровни риска `low/medium/high`
условно отображаются в клетки `1/5/9` с пояснением в `note`.

Для ручной проверки можно загрузить эталонный пример подбора подарков:

```powershell
python scripts/seed_demo.py
```

Скрипт работает только с пустой, уже мигрированной БД. Добавляет два кейса:
у первого есть эталонный отчёт, у второго отчёт `null`.
При наличии кейсов скрипт отказывается что-либо добавлять.

## OpenAPI и генерация TypeScript

Модели описаны в `app/schemas/cases.py` и `app/schemas/reports.py`.
Живая схема доступна по http://127.0.0.1:8000/openapi.json.

После изменения моделей из папки `backend`:

```powershell
python scripts/export_openapi.py
npm ci
npm run api:generate
```

Первый шаг обновляет `backend/openapi.json`, второй устанавливает инструменты
генерации из backend-lockfile, третий создаёт `backend/generated/types.gen.ts`.
Используется тот же `@hey-api/openapi-ts` 0.99.0, что установлен во frontend.
Конфигурация `openapi-ts.config.ts` и результат генерации находятся внутри backend.
Транзитивный `js-yaml` ограничен исправленной версией через `overrides`.

Сгенерированные типы структурно совместимы с эталонными; отдельные вложенные
объекты получают собственные имена типов вместо inline-описаний.

Проверить совместимость в обе стороны средствами TypeScript:

```powershell
npm run api:check
```

По умолчанию проверяются типы в соседней папке `../frontend`.
Для проверки другого frontend можно передать его путь аргументом:
`npm run api:check -- "путь/к/frontend"`.

Проверка читает исходные типы и создаёт сравнение в памяти. Файлы frontend не меняются.
После изменения контракта коммитить `openapi.json` и `generated/` вместе с моделями.

Существующий frontend всё ещё загружает локальные JSON-моки. Переключение fetch
на backend — отдельный шаг; оно не выполнялось в рамках изменения backend.
Frontend-команда `api:generate` также остаётся без изменений и читает прежний
удалённый источник, пока новая backend-ветка не опубликована.

## Тесты

Из папки `backend`, с активированной `.venv`:

```powershell
python -m unittest discover -s tests -v
npm run api:check
```

Тесты используют отдельную in-memory SQLite и временную БД для миграций:
пользовательская база не изменяется. Проверяются HTTP-ответы, данные эталона,
валидация, пять этапов анализа, ошибки, старые отчёты, отсутствие отчёта,
изоляция кейсов, удаление зависимостей и актуальность OpenAPI.

CORS разрешает `http://localhost:5173` и `http://127.0.0.1:5173`.
Другие адреса задаются через `MVPILOT_CORS_ORIGINS`, разделённые запятыми.
