# MVPilot Backend

Backend-часть проекта MVPilot.

## Стек

- Python
- FastAPI
- LangGraph
- SQLite

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
