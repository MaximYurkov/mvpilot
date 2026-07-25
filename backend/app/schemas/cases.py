from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.core.cases import CaseStage


class CaseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    audience: str | None = None
    problem: str | None = None
    stage: CaseStage = CaseStage.IDEA
    analysis_goal: str | None = None


class CaseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1)
    audience: str | None = None
    problem: str | None = None
    stage: CaseStage | None = None
    analysis_goal: str | None = None

    @model_validator(mode='after')
    def reject_null_for_required_fields(self):
        required_fields = ('title', 'description', 'stage')

        for field_name in required_fields:
            if field_name in self.model_fields_set and getattr(self, field_name) is None:
                raise ValueError(f'{field_name} cannot be null')

        return self


class CaseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    audience: str | None
    problem: str | None
    stage: CaseStage
    analysis_goal: str | None
    created_at: datetime
    updated_at: datetime
