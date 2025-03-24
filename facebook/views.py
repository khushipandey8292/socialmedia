from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import  redirect


def home(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/dashboard/')  
            else:
                return render(request, 'home.html', {'error': 'Invalid username or password'})
        return render(request, 'home.html')
    return redirect('/dashboard/')

def signup(request):
    if request.method=="POST":
            uname=request.POST.get("username")
            email=request.POST.get("email")
            pass1=request.POST.get("password1")
            pass2=request.POST.get("password2")
            if pass1!=pass2:
                return HttpResponse("your password and confrom password are not same!!")      
            else:
                my_user=User.objects.create_user(username=uname, email=email, password=pass1)
                my_user.save()
    return render(request,'signup.html') 

def dashboard(request):
    if request.user.is_superuser: 
        return render(request, "admin_dashboard.html")  
    else:
        return render(request, "dashboard.html")  

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
    