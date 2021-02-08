from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

class Course(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='its_courses')
    no_of_students = models.IntegerField(default=0)

    def increase_student(self):
        self.no_of_students +=1

    def check_capacity(self):
        if self.no_of_students < 10:
            return True
        else:
            return False
    def capacity(self):
        return self.no_of_students

    def __str__(self):
        return f"{self.name}"

class Student(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=11)
    courses = models.ManyToManyField(Course,related_name = 'its_students',blank=True)

    def __str__(self):
        return f"{self.name}"

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='its_teachers')
    gender = models.CharField(max_length=11)
    age = models.IntegerField()
    pro_pic = models.ImageField(blank = True, null = True, upload_to = "profile_pictures/")
    head = models.ForeignKey(Department,on_delete=models.PROTECT, related_name = "department_head", null=True,blank=True)

    def __str__(self):
        return f"{self.name}"