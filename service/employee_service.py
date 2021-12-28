from service.base_service import BaseService
from data.view_models import EmployeeView
from type.mapper import Mapper


class EmployeeService(BaseService):

    def __init__(self):
        super().__init__()

    def get_employee_view(self, id: int) -> EmployeeView:
        employee = self.db.get_employee(id)
        return Mapper.employee_to_view(employee)
