import os

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.analysis_runs import router as analysis_runs_router
from app.api.cases import router as cases_router
from app.api.health import router as health_router
from app.schemas.errors import ErrorResponse

app = FastAPI(
    title='MVPilot API',
    description='Backend API for MVPilot',
    version='0.1.0',
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'model': ErrorResponse,
            'description': 'Internal server error',
        },
    },
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


@app.exception_handler(Exception)
async def handle_unexpected_error(_request: Request, _error: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'detail': 'Internal server error'},
    )


@app.get('/', operation_id='getRoot')
def root():
    return {'message': 'MVPilot API'}
