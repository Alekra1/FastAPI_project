from pydantic import BaseModel, Field


class Pagination(BaseModel):
    limit: int = Field(5, ge=0)
    offset: int = Field(0, ge=0)
