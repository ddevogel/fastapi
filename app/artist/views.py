from pydantic import BaseModel, Field


class ArtistView(BaseModel):
    ArtistId: int = Field(alias="Id")
    Name: str

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
