from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.cases import router as cases_router
from app.api.health import router as health_router
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title='MVPilot API',
    description='Backend API for MVPilot',
    version='0.1.0',
    lifespan=lifespan,
)

app.include_router(health_router, prefix='/api')
app.include_router(cases_router, prefix='/api')


@app.get('/')
def root():
    return {'message': 'MVPilot API'}