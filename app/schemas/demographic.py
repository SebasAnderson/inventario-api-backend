from pydantic import BaseModel, Field, ConfigDict


class DemographicBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, examples=["Shonen"])

    model_config = ConfigDict(str_strip_whitespace=True)


class DemographicCreate(DemographicBase):
    pass


class DemographicUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=100, examples=["Seinen"])

    model_config = ConfigDict(str_strip_whitespace=True)


class DemographicResponse(DemographicBase):
    id: int = Field(..., examples=[1])

    model_config = ConfigDict(from_attributes=True)
