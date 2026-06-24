from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CaseCreate(BaseModel):
    title: str
    description: str
    audience: str | None = None
    problem: str | None = None


class CaseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    audience: str | None
    problem: str | None
    created_at: datetime
    updated_at: datetime