from pydantic import BaseModel, Field, ConfigDict


class PublisherBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, examples=["Editorial Ivrea"])

    model_config = ConfigDict(str_strip_whitespace=True)


class PublisherCreate(PublisherBase):
    pass


class PublisherUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=100, examples=["Editorial Ivrea Argentina"])

    model_config = ConfigDict(str_strip_whitespace=True)


class PublisherResponse(PublisherBase):
    id: int = Field(..., examples=[1])

    model_config = ConfigDict(from_attributes=True)
