from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class CaseFormValues(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=200)
    audience: str = Field(min_length=1, max_length=200)


class CaseUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = Field(default=None, min_length=1, max_length=200)
    audience: str | None = Field(default=None, min_length=1, max_length=200)

    @model_validator(mode='after')
    def reject_explicit_null(self):
        for field_name in self.model_fields_set:
            if getattr(self, field_name) is None:
                raise ValueError(f'{field_name} cannot be null')
        return self


class Case(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        serialize_by_alias=True,
    )

    id: int
    title: str
    description: str
    audience: str
    created_at: datetime = Field(alias='createdAt')
    updated_at: datetime = Field(alias='updatedAt')

    @field_validator('audience', mode='before')
    @classmethod
    def normalize_legacy_audience(cls, value):
        # Old database rows allowed NULL; the frontend now expects a string.
        return '' if value is None else value
