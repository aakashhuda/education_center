from django.urls import path
from . import views


app_name = 'management'
urlpatterns = [
    path("", views.home, name = 'home'),
    path("add_course", views.add_course, name = 'add_course'),
    path("save_course", views.save_course, name = 'save_course'),
    path("add_student", views.add_student, name = 'add_student'),
    path("save_student", views.save_student, name = 'save_student'),
    path("assign_course", views.assign_course, name = 'assign_course'),
    path("save_to_course", views.save_to_course, name = 'save_to_course'),
    path("add_teacher", views.add_teacher, name = 'add_teacher'),
    path("save_teacher", views.save_teacher, name = 'save_teacher'),
    path("teachers", views.list_teachers, name = 'list_teachers'),
    path("upload_pic", views.upload_pic, name = 'upload_pic'),
    path("departments/", views.departments, name = 'departments'),
    path("departments/<str:department>", views.courses, name = 'courses'),
    path("departments/<str:department>/<str:course>", views.course_details, name = 'course_details')
]