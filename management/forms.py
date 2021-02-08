from django.shortcuts import render
from django import forms
from .models import Department,Student,Course
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

choices = []
departments = Department.objects.all()
for department in departments:
    s = (department.id, department.name)
    choices.append(s)


class Course_form(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs= {'class': 'form-control form-control-sm'}),max_length=50, label='Name')
    department = forms.ChoiceField(widget=forms.Select(attrs= {'class': 'form-select form-select-sm'}), choices=choices,label='Choose department')

genders = [("male", "Male"),("female","Female"),("transgender", "Transgender")]



class Student_form(forms.Form):
    name = forms.CharField(max_length=50, label='Students Name', widget= forms.TextInput(attrs={"class":"form-control form-control-sm"}))
    gender = forms.ChoiceField(choices=genders, label="Gender", widget=forms.RadioSelect)

class Teacher_form(forms.Form):
    first_name = forms.CharField(max_length=50, label= 'First Name', widget=forms.TextInput(attrs={"class":"form-control form-control-sm"}))
    last_name = forms.CharField(max_length=50, label= 'Last Name', widget=forms.TextInput(attrs={"class":"form-control form-control-sm"}))
    department = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-select form-select-sm"}), choices=choices, label= 'Choose Department')
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=genders, label= 'Gender')
    age = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control form-control-sm"}), label= 'Age', min_value= 0, max_value=60)
    pro_pic = forms.ImageField(required=False,label="Profile Picture")
    head = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=choices,label= 'Department Head of', required=False)

class Upload_form(forms.Form):
    pro_pic = forms.ImageField(label="Upload Image: ", required=False)