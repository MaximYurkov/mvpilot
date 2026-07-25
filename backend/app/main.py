from fastapi import FastAPI

from app.api.analysis_runs import router as analysis_runs_router
from app.api.cases import router as cases_router
from app.api.health import router as health_router

app = FastAPI(
    title='MVPilot API',
    description='Backend API for MVPilot',
    version='0.1.0',
)

app.include_router(health_router, prefix='/api')
app.include_router(cases_router, prefix='/api')
app.include_router(analysis_runs_router, prefix='/api')


@app.get('/')
def root():
    return {'message': 'MVPilot API'}
