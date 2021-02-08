from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login:login'))
    else:
        return HttpResponseRedirect(reverse('management:home'))
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)
        if user:
            login(request,user)
            for key, value in request.session.items():
                print(key,value)
            print(request.session['_auth_user_id'])
            print(request.user)
            print(request.user.id)
            if 'next' in request.POST:
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('management:home'))
        else:
            return render(request, 'login/login.html')

    return render(request, "login/login.html")

def logout_view(request):
    logout(request)
    return render(request, "login/login.html")
