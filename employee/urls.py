from django.contrib import admin
from django.urls import path
from .views import (
    DepartmentDetailView,
    DepartmentListView,

    EmployeeListView,
    EmployeeDetailView,
    EmployeeDepartmentView,

    ProjectListView,
    ProjectDetailView,
    ProjectMemberView,
    ProjectBudgetView,
    ProjectStatusView,

    highestSalary,
    secondHighestSalary,
    total_salary_by_department
)

urlpatterns = [
    path('departments/', DepartmentListView.as_view(), name='department-list-create'),
    path('departments/<int:id>/', DepartmentDetailView.as_view(), name='department-update-delete'),

    path('employees/', EmployeeListView.as_view(), name='employee-list-create'),
    path('employees/<int:id>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/<int:id>/department', EmployeeDepartmentView.as_view(), name='employee-detail'),

    path('projects/', ProjectListView.as_view(), name='project-list-create'),
    path('projects/<int:id>/', ProjectDetailView.as_view(), name='project-list-create'),
    path('projects/<int:id>/add-member/', ProjectMemberView.as_view(), name='project-add-member'),
    path('projects/<int:id>/budget/', ProjectBudgetView.as_view(), name= 'project-budget'),
    path('projects/<str:filter_status>/', ProjectStatusView.as_view(), name= 'project-status'),
    
    path('employees/highest-salary/', highestSalary, name= 'highest-salary'),
    path('employees/second-high-salary/', secondHighestSalary, name= 'second-highest-salary'),

    path('departments/total-salary/', total_salary_by_department , name='department-total-salary'),
]
