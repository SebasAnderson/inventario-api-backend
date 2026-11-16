from pydantic import BaseModel, Field, ConfigDict


class PublisherBase(BaseModel):
    nombre: str = Field(..., max_length=100, examples=["Editorial Ivrea"])


class PublisherCreate(PublisherBase):
    pass


class PublisherUpdate(BaseModel):
    nombre: str | None = Field(None, max_length=100, examples=["Editorial Ivrea Argentina"])


class PublisherResponse(PublisherBase):
    id: int = Field(..., examples=[1])

    model_config = ConfigDict(from_attributes=True)
