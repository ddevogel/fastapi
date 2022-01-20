from fastapi import APIRouter, Depends, HTTPException
from .views import EmployeeView

from .service import get_employee_view
from ..dependencies import check_404, get_state, verify_token


employees = APIRouter(
    prefix="/employees",
    tags=["employees"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}},
)


# https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/
@employees.get("/{id}", response_model=EmployeeView)
async def employee(id: int, state=Depends(get_state)):
    response = get_employee_view(db_session=state.db, id=id)
    return check_404(response)
