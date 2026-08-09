# MVPilot Backend

Backend-часть проекта MVPilot.

## Стек

* Python
* FastAPI
* SQLite
* SQLAlchemy

Мультиагентная система и LangGraph пока не подключены. Анализ выполняется
локальной mock-функцией без LLM.

## Локальный запуск

Перейти в папку backend:

```powershell
cd backend
```

Создать виртуальное окружение:

```powershell
python -m venv .venv
```

Активировать окружение:

```powershell
.\.venv\Scripts\Activate.ps1
```

Установить зависимости:

```powershell
pip install -r requirements.txt
```

Применить миграции базы данных:

```powershell
alembic upgrade head
```

Запустить сервер:

```powershell
uvicorn app.main:app --reload
```

После запуска API доступно по адресу:

```text
http://127.0.0.1:8000
```

Swagger-документация:

```text
http://127.0.0.1:8000/docs
```

## Контекст продуктового кейса

Кроме названия, описания, аудитории и проблемы кейс содержит:

* `stage` — текущую стадию: `idea`, `validation`, `prototype`, `mvp` или
  `launched`;
* `analysis_goal` — сформулированную пользователем цель анализа.

Если стадия не передана, используется `idea`. Оба поля можно изменить через
`PATCH /api/cases/{case_id}`.

## Mock-анализ

Основной сценарий:

1. Создать кейс через `POST /api/cases`.
2. Запустить анализ через `POST /api/cases/{case_id}/analysis-runs`.
3. Получить запуск через `GET /api/analysis-runs/{run_id}`.

Все запуски одного кейса можно получить через:

```text
GET /api/cases/{case_id}/analysis-runs
```

Mock-анализ не обращается к внешним сервисам. Он сразу формирует тестовый
структурированный отчёт и сохраняет его в SQLite.

Каждый запуск содержит пять этапов:

1. `planner`;
2. `market_analyst`;
3. `product_manager`;
4. `critic`;
5. `editor`.

Для этапа сохраняются статус, результат, ошибка, время старта и завершения.
Этапы возвращаются вместе с `AnalysisRun` через API.

Отчёт содержит:

* план анализа и используемые гипотезы;
* проблему, аудиторию и ценностное предложение;
* JTBD и Lean Canvas;
* MVP, backlog и roadmap;
* риски, критику и рекомендации;
* Markdown-версию итогового продуктового кейса.

Формат каждого раздела описан Pydantic-схемами и отображается в Swagger.

## OpenAPI и подключение frontend

При запущенном backend спецификация доступна по адресу:

```text
http://127.0.0.1:8000/openapi.json
```

Её сохранённая копия находится в `openapi.json`. После изменения API обновить
файл из папки `backend`:

```powershell
python scripts/export_openapi.py
```

Локальные frontend-адреса `http://localhost:5173` и
`http://127.0.0.1:5173` разрешены через CORS. Другие адреса можно передать
через переменную `MVPILOT_CORS_ORIGINS`, разделяя их запятыми.

## Миграции базы данных

Alembic хранит последовательность изменений структуры БД в
`migrations/versions/`.

Показать текущую версию базы:

```powershell
alembic current
```

Создать миграцию после изменения SQLAlchemy-моделей:

```powershell
alembic revision --autogenerate -m "описание изменения"
```

Проверить созданный файл миграции и применить его:

```powershell
alembic upgrade head
```

## Тесты

Из папки `backend` выполнить:

```powershell
python -m unittest discover -s tests -v
```
