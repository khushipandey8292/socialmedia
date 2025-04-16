from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import  redirect
from .tasks import send_otp_email 
import random
def home(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                otp = str(random.randint(100000, 999999))
                request.session['otp_code'] = otp
                request.session['otp_user_id'] = user.id
                send_otp_email.delay(user.email, otp)
                return redirect('verify_otp')
                # login(request, user)
                # return redirect('/dashboard/')  
            else:
                return render(request, 'home.html', {'error': 'Invalid username or password'})
        else:
            return render(request, 'home.html')
    else:
        return redirect('/dashboard/')

def verify_otp(request):
    if request.method == "POST":
        input_otp = request.POST.get('otp')
        real_otp = request.session.get('otp_code')
        user_id = request.session.get('otp_user_id')

        if input_otp == real_otp:
            user = User.objects.get(id=user_id)
            login(request, user)
            # clear session
            request.session.pop('otp_code')
            request.session.pop('otp_user_id')
            return redirect('/dashboard/')
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})
    
    return render(request, 'verify_otp.html')

def signup(request):
    if request.method=="POST":
            uname=request.POST.get("username")
            email=request.POST.get("email")
            pass1=request.POST.get("password1")
            pass2=request.POST.get("password2")
            if pass1!=pass2:
                return HttpResponse("your password and confirm password are not same!!")      
            else:
                my_user=User.objects.create_user(username=uname, email=email, password=pass1)
                my_user.save()
                return redirect('home')
    return render(request,'signup.html') 

def dashboard(request):
    if request.user.is_authenticated:
        print("User:", request.user)
        if request.user.is_superuser: 
            return render(request, "admin_dashboard.html")  
        else:
            return render(request, "dashboard.html")  
    else:
        return render(request,'home.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
    