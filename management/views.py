from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from .models import Department,Course,Student,Teacher
from .forms import Course_form,Student_form,Teacher_form,Upload_form
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist,EmptyResultSet
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, "management/home.html")

@login_required(login_url='login:login')
def add_course(request):
    choices = []
    try:
        departments = Department.objects.all()
    except Department.DoesNotExist:
        return HttpResponseRedirect(reverse('management:departments'))
    for department in departments:
        s = (department.id, department.name)
        choices.append(s)

    return render(request, "management/index.html",{
            "form":Course_form()
        })

def save_course(request):
    if request.method == "POST":
        form = Course_form(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name'].capitalize()
            dep_id = int(form.cleaned_data['department'])
            department = Department.objects.get(pk = dep_id)
            try:
                check_course = Course.objects.get(name=name)
            except:
                course = Course(name = name, department=department)
                course.save()
                return render(request, "management/index.html",{
                    "form": Course_form(),
                    "message": f"{name} course added to {department} department"
                })
            else:
                return render(request, "management/index.html",{
                    "form":form,
                    "message": f"{name} course already exists!"
                })
        else:
            return HttpResponseRedirect(reverse('management:add_course'))
    else:
        return HttpResponseRedirect(reverse('management:add_course'))

@login_required(login_url='login:login')
def add_student(request):
    return render(request, "management/add_student.html", {
        "form":Student_form()
    })
    
def save_student(request):
    if request.method == "POST":
        form = Student_form(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name'].capitalize()
            gender = form.cleaned_data['gender']
            try:
                check_student = Student.objects.get(name=name)
            except Student.DoesNotExist:
                student = Student(name=name,gender=gender)
                student.save()
                return render(request, "management/add_student.html",{
                    "form":Student_form(),
                    "message":"New Student Registered"
                })
            else:
                return render(request, "management/add_student.html",{
                    "form":form,
                    "message":"Student already registered!"
                })
        else:
            return render(request, "management/add_student.html", {
                "form":form,
                "message":"Invalid form! Please fill up the information again."
            })
    else:
        return HttpResponseRedirect(reverse('management:add_student'))

@login_required(login_url='login:login')
def assign_course(request):
    try:
        courses = Course.objects.all()
        students = Student.objects.all()
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('management:index'))
    return render(request, "management/assign_course.html", {
        "courses":courses,
        "students":students
    })
def save_to_course(request):
    if request.method == 'POST':
        c = request.POST["course"]
        s = request.POST["student"]
        print(c,s)
        try:
            course = Course.objects.get(name=c)
            student = Student.objects.get(name=s)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('management:assign_course'))
        try:
            match = course.its_students.all()
        except Course.DoesNotExist:
            return HttpResponseRedirect(reverse('management:assign_course'))
        if student in match :
            return HttpResponseRedirect(reverse('management:assign_course'))
        else:
            student.courses.add(course)
            course.increase_student()
            course.save()
            return render(request, "management/assign_course.html",{
                "message":f"Assigned {course} to {student}"
            })
    return HttpResponseRedirect(reverse('management:index'))

@login_required(login_url='login:login')
def add_teacher(request):
    choices = []
    try:
        departments = Department.objects.all()
    except Department.DoesNotExist:
        return HttpResponseRedirect(reverse('management:departments'))
    for department in departments:
        s = (department.id, department.name)
        choices.append(s)
        return render(request, 'management/add_teacher.html', {
        "form": Teacher_form(),
        "message": None
    })

def save_teacher(request):
    if request.method == 'POST':
        form = Teacher_form(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name'].capitalize()
            last_name = form.cleaned_data['last_name'].capitalize()
            name = first_name + " " + last_name
            department_id = form.cleaned_data['department']
            gender = form.cleaned_data['gender']
            age = form.cleaned_data['age']
            department = Department.objects.get(pk=department_id)
            pro_pic = form.cleaned_data['pro_pic']
            dept_id = form.cleaned_data['head'][0]
            head = Department.objects.get(pk=dept_id)
            try:
                teacher = Teacher.objects.get(name=name)
                return render(request, 'management/add_teacher.html', {
                    "form":form,
                    "message": "Teacher already registered!"
                })
            except:
                teacher = Teacher(name=name,department=department,gender=gender,age=age,pro_pic=pro_pic,head=head)
                teacher.save()
                return HttpResponseRedirect(reverse('management:add_teacher'))
        else:
            return render(request, 'management/add_teacher.html', {
                "form":form,
                "message":"Form is not valid!"
            })

    return HttpResponseRedirect(reverse("management:add_teacher"))

def list_teachers(request):
    try:
        teachers = Teacher.objects.all()

    except Teacher.EmptyResultSet:
        return render(request, "management/teachers.html")

    return render(request, "management/teachers.html", {
        "teachers": teachers,
        "form": Upload_form()
    })
@login_required(login_url='login:login')
def upload_pic(request):
    if request.method == "POST":
        form = Upload_form(request.POST,request.FILES)

        if form.is_valid():
            pic = form.cleaned_data['pro_pic']
            name = request.POST['name']
            teacher = Teacher.objects.get(name = name)
            teacher.pro_pic = pic
            teacher.save()
            return HttpResponseRedirect(reverse('management:list_teachers'))

        else:
            return HttpResponseRedirect(reverse('management:list_teachers'))
    else:
        return HttpResponseRedirect(reverse('management:list_teachers'))

def departments(request):
    try:
        departments = Department.objects.all()
    except EmptyResultSet:
        return HttpResponse('No Departments found!')
    return render(request, 'management/departments.html', {
        "departments": departments
    })

def courses(request, department):
    try:
        dep = Department.objects.get(name=department.capitalize())
    except Department.DoesNotExist:
        return HttpResponseRedirect(reverse('management:departments'))
    courses = dep.its_courses.all()
    return render(request, "management/courses.html", {
        "courses":courses,
        "department":department
    })
def course_details(request,department,course):
    try:
        course_details = Course.objects.get(name = course)
    except Course.DoesNotExist:
        return HttpResponse("Course not found!")
    return render(request, "management/course_details.html",{
        "course_details": course_details,
        "students": course_details.its_students.all()
    })
