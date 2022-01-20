from typing import ForwardRef
from pydantic import BaseModel, Field

# https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
EmployeeView = ForwardRef('EmployeeView')


class EmployeeView(BaseModel):
    EmployeeId: int = Field(alias="Id")
    LastName: str
    FirstName: str
    Title: str
    Phone: str
    Email: str
    Manager: 'EmployeeView' = None

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


EmployeeView.update_forward_refs()
