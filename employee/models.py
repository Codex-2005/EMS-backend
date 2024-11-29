from django.db import models


    
class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    name = models.CharField(max_length=200)
    salary = models.FloatField()
    designation = models.CharField(max_length=200)
    department = models.ForeignKey(Department,on_delete= models.CASCADE, related_name='emp_dpt')
    address = models.CharField(max_length=200)
    # projects = models.ManyToManyField('Project', related_name='employees')
    projects = models.ManyToManyField('Project', related_name='employees', blank=True)


    def __str__(self):
        return self.name

class Project(models.Model):
    NEW = 'NEW'
    ON_GOING = 'ON-GOING'
    ENDED = 'ENDED'
    STATUS_CHOICES = [
        (NEW, 'New'),
        (ON_GOING, 'On going'),
        (ENDED, 'Ended'),
    ]

    name = models.CharField(max_length=200)
    # team = models.ManyToManyField('Employee', related_name='team_projects')
    team = models.ManyToManyField('Employee', related_name='team_projects')

    team_lead = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=NEW)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name