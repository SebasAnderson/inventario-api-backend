from pydantic import BaseModel, Field, ConfigDict


class FranchiseBase(BaseModel):
    nombre: str = Field(..., max_length=100, examples=["Dragon Ball"])


class FranchiseCreate(FranchiseBase):
    pass


class FranchiseUpdate(BaseModel):
    nombre: str | None = Field(None, max_length=100, examples=["Dragon Ball Super"])


class FranchiseResponse(FranchiseBase):
    id: int = Field(..., examples=[1])

    model_config = ConfigDict(from_attributes=True)
