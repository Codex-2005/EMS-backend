from django.db.models import Max,Sum
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Department, Employee, Project
from .serializers import DepartmentSerializer, EmployeeSerializer, ProjectSerializer
from django.utils import timezone

class DepartmentListView(APIView):
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDetailView(APIView):
    def put(self,request,id):
        try:
            department = Department.objects.get(id = id)
        except Department.DoesNotExist:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DepartmentSerializer(department, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request, id):
        try:
            department = Department.objects.get(id = id)
            if department.emp_dpt.exists():
                return Response({"error": "Department cannot be delete as it has employees"}, status=status.HTTP_400_BAD_REQUEST)
            department.delete()
            return Response({"messag": "Department is deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Department.DoesNotExist:
            return Response({"error" : "Deparment does not found"}, status= status.HTTP_404_NOT_FOUND)
        
    def get(self,request,id):
        try:
            department = Department.objects.get(id = id)
            employees = department.emp_dpt.all()
            dept_data = {
                'id' : department.id,
                'name' : department.name,
                'employees' : [{"id" : emp.id, "name" : emp.name} for emp in employees ] if employees else "No employees available with department"
            }
            return Response(dept_data, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response({"error" : "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        



# Employee 
# POST /employees/ to create an employee
# GET /employees/ to get all employee data

class EmployeeListView(APIView):
    def get(self,request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many = True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    def post(self,request):
        serializer = EmployeeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# PUT /employees/<id>/ to update employee data by ID
# GET /employees/<id>/ to get employee data by ID
# DELETE /employees/<id>/ to delete an employee
class EmployeeDetailView(APIView):
    def get(self,request,id):
        employee = Employee.objects.get(id = id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def delete(self, request, id):
        try:
            employee = Employee.objects.get(id=id)
            employee.delete()
            return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self,request,id):
        try:
            employee = Employee.objects.get(id = id)
        except Employee.DoesNotExist:
            return Response({"error" : "Employee does not found"}, status= status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee , data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message' : 'Employee Updated'}, status=status.HTTP_201_CREATED)
        return Response({"error" : "Invalid"}, status= status.HTTP_400_BAD_REQUEST)
        
# GET /employees/<id>/department/ to get department details by employee ID
class EmployeeDepartmentView(APIView):
    def get(self, request, id):
        try:
            employee = Employee.objects.get(id=id)
            department = employee.department  # Access the related department
            department_data = {
                'emp_id' : employee.id,
                'emp_name' : employee.name,
                'dpt_id': department.id,
                'dpt_name': department.name
            }
            return Response(department_data)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)


# Project Views
# POST /projects/ to create a new project
# GET /projects/ to get all projects (with team members data)

class ProjectListView(APIView):
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            # Save the project and get the instance
            project = serializer.save()

            # Update `projects` field for team members
            team = request.data.get('team', [])
            team_lead_id = request.data.get('team_lead')

            # Add the project to each employee's `projects` field
            if team:
                employees = Employee.objects.filter(id__in=team)
                for employee in employees:
                    employee.projects.add(project.id)

            # Add the project to the team_lead's `projects` field
            if team_lead_id:
                team_lead = Employee.objects.filter(id=team_lead_id).first()
                if team_lead:
                    team_lead.projects.add(project.id)
            # print(project.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProjectDetailView(APIView):
    def get(self,request,id):
        try:
            project = Project.objects.get(id = id)
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({"error" : "Project does not exist"}, status= status.HTTP_404_NOT_FOUND)
    def put(self,request,id):
        try:
            project = Project.objects.get(id = id)
        except Project.DoesNotExist:
            return Response({"error" : "Project Does not exist"}, status= status.HTTP_404_NOT_FOUND)
        
        if "status" in request.data:
            new_status = request.data['status']
            if new_status not in [choice[0] for choice in Project.STATUS_CHOICES]:
                # print([choice[0] for choice in Project.STATUS_CHOICES])
                return Response({"error" : "Invalid Choice"}, status= status.HTTP_404_NOT_FOUND)
            project.status = new_status
            project.save()
            return Response({'message' : 'Status updated successfuly'}, status= status.HTTP_201_CREATED)
        return Response({'error': "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        try:
            project = Project.objects.get(id = id)
            if project.end_date > timezone.now().date():
                return Response({'error' : 'Project cannot be delete before its end date'})
            project.delete()
            return Response({'message' : 'Project deleted'}, status= status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({'error' : 'Project Not Found'}, status= status.HTTP_404_NOT_FOUND)
        
class ProjectMemberView(APIView):
    def put(self,request, id):
        try:
            project = Project.objects.get(id = id)
    
        except Project.DoesNotExist:
            return Response({'error' : 'Project Not Found'}, status= status.HTTP_404_NOT_FOUND)

        member_id = request.data.get("member_id")
        try:
            member = Employee.objects.get(id = member_id)
        
        except:
            return Response({'error' : 'Member Not Found'}, status= status.HTTP_404_NOT_FOUND)
        
        if member_id in [member.id for member in project.team.all()]:
            return Response({'error' : 'Member aready in team'})
        project.team.add(member_id)
        return Response({'message' : 'Member added successfuly'})
    
class ProjectBudgetView(APIView):
    def get(self,request,id):
        try:
            project = Project.objects.get(id = id)
            total_budget = sum(member.salary for member in project.team.all())
            return Response({'Budget' : total_budget})
        except Project.DoesNotExist:
            return Response({'error' : 'Project Not Found'}, status= status.HTTP_404_NOT_FOUND)

class ProjectStatusView(APIView):
    def get(self,request,filter_status):
        if filter_status not in [choice[0] for choice in Project.STATUS_CHOICES]:
            return Response({'error' : 'Invalid Status'}, status=status.HTTP_404_NOT_FOUND)
    
        project = Project.objects.filter(status = filter_status)
        serializer = ProjectSerializer(project, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
# GET /employees/highest-salary/ to get the highest salary holders
@api_view(['GET'])
def highestSalary(request):
    highest_salary_dict = Employee.objects.aggregate(Max('salary'))
    if highest_salary_dict is None:
        return Response({"message": "No employees found"}, status=status.HTTP_404_NOT_FOUND)
    highest_salary_value = highest_salary_dict['salary__max']
    employee = Employee.objects.filter(salary = highest_salary_value)
    serializer = EmployeeSerializer(employee, many = True)
    return Response(serializer.data)

# GET /employees/second-highest-salary/ to get the second-highest salary holder grouped by department
@api_view(['GET'])
def secondHighestSalary(request):
    sorted_emp = Employee.objects.order_by('-salary')
    if len(sorted_emp) >= 2:
        sorted_emp = sorted_emp[1:2]
    serializer = EmployeeSerializer(sorted_emp, many= True)
    return Response(serializer.data)


# GET /departments/total-salary/ to get the total salary of employees under each department
@api_view(['GET'])
def total_salary_by_department(request):
    departments = Department.objects.annotate(total_salary = Sum('emp_dpt__salary')) #here is 2 _ _ at salary
    data = [
        {
            'department' : department.name,
            'total salary' : department.total_salary,
        }

        for department in departments
    ]
    return Response(data)