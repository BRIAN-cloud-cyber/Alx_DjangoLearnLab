from django.db import models

class student(models.Model):

    REGION=[
        ('NA', 'North America'),
        ('SA', 'South America'),
        ('EU', 'Europe'),
        ('AS', 'Asia'),
        ('AF', 'Africa'),
        ('OC', 'Oceania'),
    ]
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    enrollment_date = models.DateField()
    region = models.CharField(max_length=2, choices=REGION, default='NA')

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.region}"
    
class course(models.Model):
    students=models.ManyToManyField(student, on_delete=models.CASCADE) # Many-to-Many relationship with student 
    title = models.CharField(max_length=100)
    description = models.TextField()
    credits = models.IntegerField()
    duration_weeks = models.IntegerField()
    SET_DEFAULT = 'NULL'

    #optimizing database performance
    prefetching_students=student.objects.prefetch_related('students')

    def __str__(self):
        return self.title
