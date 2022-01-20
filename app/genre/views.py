from pydantic import BaseModel, Field


class GenreView(BaseModel):
    GenreId: int = Field(alias="Id")
    Name: str

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
