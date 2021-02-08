from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
    return render(request, "signup/index.html",{
        "message":""
    })

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        try:
            username = User.objects.get(username=username)
        except:
            pass
        else:
            return render(request, "signup/index.html", {
                "message": "Username already taken!"
            })
        try:
            email = User.objects.get(email=email)
        except:
            pass
        else:
            return render(request, "signup/index.html", {
                "message": "Email already taken!"
            })
        user = User.objects.create_user(username = username,password=password,email=email,first_name=first_name,last_name=last_name)
        user.save()
        return HttpResponseRedirect(reverse('login:login'))
            
    else:
        return HttpResponseRedirect(reverse('signup:signup'))