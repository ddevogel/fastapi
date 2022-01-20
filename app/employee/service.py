from ..database.service import SessionLocal
from ..models import Employee
from .views import EmployeeView


def employee_to_view(employee: Employee) -> EmployeeView:
    if employee is None:
        return None
    view = EmployeeView.from_orm(employee)
    view.__setattr__("Manager", view.from_orm(employee.parent))
    return view


def get_employee_view(db_session: SessionLocal, id: int) -> EmployeeView:
    employee = db_session.get_employee(id)
    return employee_to_view(employee)
