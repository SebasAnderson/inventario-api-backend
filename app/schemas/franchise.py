from pydantic import BaseModel, Field, ConfigDict


class FranchiseBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, examples=["Dragon Ball"])

    model_config = ConfigDict(str_strip_whitespace=True)


class FranchiseCreate(FranchiseBase):
    pass


class FranchiseUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=100, examples=["Dragon Ball Super"])

    model_config = ConfigDict(str_strip_whitespace=True)


class FranchiseResponse(FranchiseBase):
    id: int = Field(..., examples=[1])

    model_config = ConfigDict(from_attributes=True)
