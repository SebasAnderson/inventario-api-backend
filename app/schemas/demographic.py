from pydantic import BaseModel, Field, ConfigDict


class DemographicBase(BaseModel):
    nombre: str = Field(..., max_length=100, examples=["Shonen"])


class DemographicCreate(DemographicBase):
    pass


class DemographicUpdate(BaseModel):
    nombre: str | None = Field(None, max_length=100, examples=["Seinen"])


class DemographicResponse(DemographicBase):
    id: int = Field(..., examples=[1])

    model_config = ConfigDict(from_attributes=True)
