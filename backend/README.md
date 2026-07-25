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

## Тесты

Из папки `backend` выполнить:

```powershell
python -m unittest discover -s tests -v
```
