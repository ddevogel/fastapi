from fastapi import APIRouter, Depends

from ..dependencies import check_404, get_state
from .service import get_employee_view
from .views import EmployeeView

employees = APIRouter(
    prefix="/employees",
    tags=["employees"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@employees.get("/{id}", response_model=EmployeeView)
async def employee(id: int, state=Depends(get_state)):
    response = get_employee_view(db_session=state.db, id=id)
    return check_404(response)
