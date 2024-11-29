from rest_framework import serializers
from .models import Employee, Department, Project


# Employee Serializer
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Employee.objects.all()
    )  # Accepts list of Employee IDs
    team_lead = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all()
    )  # Accepts a single Employee ID

    class Meta:
        model = Project
        fields = '__all__'

        