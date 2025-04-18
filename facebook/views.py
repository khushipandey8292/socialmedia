from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import  redirect
import random
from django.contrib.auth.decorators import login_required
from .models import CustomUser

def home(request):
        return render(request, 'home.html')

def register_customer(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            user_type='customer',
            is_verified=True 
        )
        return redirect('login')
    return render(request, 'register_customer.html')
from django.core.mail import send_mail

def generate_otp():
    return str(random.randint(100000, 999999))
def register_seller(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            user_type='seller',
            is_verified=True  
        )
        otp = generate_otp()
        UserOTP.objects.create(user=user, otp=otp)
        send_mail(
                subject='Your OTP for Account Verification',
                message=f'Your OTP is {otp}',
                from_email='your_email@gmail.com',
                recipient_list=[user.email],
            )
        request.session['username'] = user.username  
        messages.success(request, "OTP sent to your email.")
        return redirect('verify_otp')

        # return redirect('verify_seller_otp')
    return render(request, 'register_seller.html')


from .forms import OTPForm
from .models import UserOTP
def verify_otp(request):
    username = request.session.get('username')
    if not username:
        return redirect('signup')

    form = OTPForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            user = CustomUser.objects.filter(username=username).first()
            if user:
                real_otp = UserOTP.objects.filter(user=user).first()
                if real_otp and entered_otp == real_otp.otp:
                    user.is_active = True
                    user.save()
                    real_otp.delete()
                    messages.success(request, "OTP verified! You can now login.")
                    return redirect('login')
                else:
                    messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'verify_otp.html', {'form': form})


def register_admin(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = CustomUser.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            is_verified=True ,
            user_type='admin',
        )
        return redirect('login')
    return render(request, 'register_admin.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user.user_type == 'seller' and not user.is_verified:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("Invalid credentials")
    return render(request, 'login.html')

@login_required
def dashboard(request):
    user = request.user
    if user.is_superuser:
        return render(request, 'admin_dashboard.html')
    elif user.user_type == 'seller':
        return render(request, 'seller_dashboard.html')
    elif user.user_type == 'customer':
        return render(request, 'customer_dashboard.html')
    else:
        return HttpResponse("Unknown user type.")


# Logout
def user_logout(request):
    logout(request)
    return redirect('login')
