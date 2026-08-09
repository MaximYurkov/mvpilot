import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analysis_runs import router as analysis_runs_router
from app.api.cases import router as cases_router
from app.api.health import router as health_router

app = FastAPI(
    title='MVPilot API',
    description='Backend API for MVPilot',
    version='0.1.0',
)

default_cors_origins = (
    'http://localhost:5173',
    'http://127.0.0.1:5173',
)
cors_origins = [
    origin.strip()
    for origin in os.getenv(
        'MVPILOT_CORS_ORIGINS',
        ','.join(default_cors_origins),
    ).split(',')
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(health_router, prefix='/api')
app.include_router(cases_router, prefix='/api')
app.include_router(analysis_runs_router, prefix='/api')


@app.get('/', operation_id='getRoot')
def root():
    return {'message': 'MVPilot API'}
