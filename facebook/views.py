from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import  redirect
import random
import datetime
from .forms import AddressForm ,CategoryForm, SubcategoryForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import CustomUser,UserOTP,Category,Myproduct,Subcategory,Cart,Myorders
from .forms import Myform ,OTPForm,MyProductForm
from .tasks import send_seller_status_email
import string
def home(request):
    data=Category.objects.all().order_by('-id')[0:18]
    md={"cdata":data}
    return render(request, 'home.html',md)

def about(request):
    return render(request,'about.html')

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

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
                if real_otp:
                    if real_otp.is_expired:
                        messages.error(request, "OTP has expired. Please request a new one.")
                    elif entered_otp == real_otp.otp:
                        user.is_active = True
                        user.save()
                        real_otp.delete()
                        return redirect('login')
                    else:
                        messages.error(request, "Invalid OTP. Please try again.")
    
    if request.method == "GET" and 'resend_otp' in request.GET:
        user = CustomUser.objects.filter(username=username).first()
        if user:
            otp = generate_otp()
            UserOTP.objects.update_or_create(user=user, defaults={'otp': otp})
            send_mail(
                "Your OTP Code",
                f"Your OTP code is {otp}",
                'from@example.com', 
                [user.email],
                fail_silently=False,
            )
            messages.success(request, "A new OTP has been sent to your email.")
        return redirect('verify_otp')  

    return render(request, 'verify_otp.html', {'form': form})


def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        if role == 'customer':
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type='customer',
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

        elif role == 'seller':
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type='seller',
                is_verified=False 
            )
            return HttpResponse("Seller registered successfully. Please wait for admin verification.")

        elif role == 'admin':
            user = CustomUser.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                user_type='admin',
                is_verified=True
            )
            return redirect('login')

        else:
            messages.error(request, "Invalid role selected.")
            return redirect('register_user')

    return render(request, 'register_user.html')


def user_login(request):
    form = Myform(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            role = request.POST.get('role')  

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.user_type != role:
                    return render(request, 'login.html', {
                        'form': form,
                        'error': 'Invalid role selected for this account.'
                    })

                if role == 'seller':
                    if not user.is_verified:
                        return HttpResponse("Seller account not verified by admin yet.")
                    else:
                        login(request, user)
                        return redirect('seller_dashboard')
                elif role == 'customer':
                    login(request, user)
                    return redirect('customer_dashboard')
                elif role == 'admin':
                    login(request, user)
                    return redirect('admin_dashboard')
                else:
                    return render(request, 'login.html', {
                        'form': form,
                        'error': 'Invalid role.'
                    })
            else:
                return render(request, 'login.html', {
                    'form': form,
                    'error': 'Invalid username or password.'
                })
        else:
            return render(request, 'login.html', {
                'form': form,
                'error': 'Invalid form submission.'
            })

    return render(request, 'login.html', {'form': form})


def seller_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'seller':
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'admin':
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper

@login_required
@seller_required
def seller_dashboard(request):
    products = Myproduct.objects.filter(seller=request.user)
    return render(request, 'seller_dashboard.html', {'products': products})

@login_required
def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')

@admin_required
@login_required
def admin_dashboard(request):
    sellers = CustomUser.objects.filter(user_type='seller')
    customers = CustomUser.objects.filter(user_type='customer')
    products = Myproduct.objects.all()
    return render(request, 'admin_dashboard.html',{'sellers': sellers,'customers': customers,'products': products})

@login_required
def approve_seller(request, seller_id):
    if request.user.user_type != 'admin':
        return HttpResponse("Unauthorized access.")

    seller = get_object_or_404(CustomUser, id=seller_id, user_type='seller')
    seller.is_verified = True
    seller.save()
    send_seller_status_email.delay(seller.email, 'approved')
    return redirect('admin_dashboard') 

@login_required
def unapprove_seller(request, seller_id):
    if request.user.user_type != 'admin':
        return HttpResponse("Unauthorized access.")
    
    seller = get_object_or_404(CustomUser, id=seller_id, user_type='seller')
    seller.is_verified = False
    seller.save()
    send_seller_status_email.delay(seller.email, 'unapproved')
    return redirect('admin_dashboard') 

@login_required
def delete_seller(request, seller_id):
    if request.user.user_type != 'admin':
        return HttpResponse("Unauthorized access.")
    
    seller = get_object_or_404(CustomUser, id=seller_id, user_type='seller')
    seller.delete()
    return redirect('admin_dashboard') 

@login_required
def delete_customer(request, customer_id):
    if request.user.user_type != 'admin':
        return HttpResponse("Unauthorized access.")

    customer = get_object_or_404(CustomUser, id=customer_id, user_type='customer')
    customer.delete()
    return redirect('admin_dashboard')  

def user_logout(request):
    logout(request)
    return redirect('login')

def product(request):
    catid=request.GET.get('cid')
    subcatid=request.GET.get('sid')
    sdata=Subcategory.objects.all().order_by('-id')
    if subcatid is not None:
        pdata=Myproduct.objects.all().filter(subcategory_name=subcatid)
    elif catid is not None:
        pdata=Myproduct.objects.all().filter(product_category=catid)
    else :
        pdata=Myproduct.objects.all().order_by('-id')
    md={"subcat":sdata,"pdata":pdata}
    return render(request,'product.html',md)


@login_required
def add_category(request):
    if request.user.user_type != 'seller':
        return redirect('home')
    
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.seller = request.user
            category.save()
            return redirect('seller_dashboard')
    else:
        form = CategoryForm()
    
    return render(request, 'category.html', {'form': form})



@login_required
def add_subcategory(request):
    if request.user.user_type != 'seller':
        return HttpResponse("<script>alert('Only sellers can add subcategories');location.href='/'</script>")
    
    if request.method == 'POST':
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            form.save()  # Save the subcategory
            return redirect('seller_dashboard')  # Redirect to the seller dashboard after saving
    else:
        form = SubcategoryForm()
    
    return render(request, 'subcategory.html', {'form': form})


@login_required
@seller_required
def add_product(request):
    form = MyProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        product = form.save(commit=False)
        product.seller = request.user
        product.save()
        return redirect('seller_dashboard')
    return render(request, 'product_form.html', {'form': form})

@login_required
@seller_required
def edit_product(request, pk):
    product = get_object_or_404(Myproduct, pk=pk, seller=request.user)
    form = MyProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('seller_dashboard')
    return render(request, 'product_form.html', {'form': form,'is_edit': True})

@login_required
@seller_required
def delete_product(request, pk):
    product = get_object_or_404(Myproduct, pk=pk, seller=request.user)
    product.delete()
    return redirect('seller_dashboard')


@login_required
@admin_required
def delete_product_admin(request, pk):
    product = get_object_or_404(Myproduct, pk=pk)
    product.delete()
    return redirect('admin_dashboard')


from django.utils import timezone

@login_required
def Mycart(request):
    if request.user.user_type != 'customer':
        return HttpResponse("<script>alert('Only customers can access the cart');location.href='/'</script>")

    if request.method == "GET" and request.GET.get('qt'):
        qt = int(request.GET.get('qt'))
        pname = request.GET.get('pname')
        ppic = request.GET.get('ppic')
        pw = request.GET.get('pw')
        price = int(request.GET.get('price'))
        total_price = qt * price

        if qt > 0:
            Cart.objects.create(
                user=request.user,
                product_name=pname,
                quantity=qt,
                price=price,
                total_price=total_price,
                product_picture=ppic,
                pw=pw,
                added_date=timezone.now().date()
            )
            request.session['cartitem'] = Cart.objects.filter(user=request.user).count()
            return HttpResponse("<script>alert('Your item was added successfully');location.href='/product/'</script>")
        else:
            return HttpResponse("<script>alert('Add product quantity to your cart');location.href='/product/'</script>")

    return render(request, 'mycart.html')


@login_required
def cartitem(request):
    if request.user.user_type != 'customer':
        return HttpResponse("<script>alert('Only customers can view the cart');location.href='/'</script>")

    cid = request.GET.get('cid')
    cartdata = Cart.objects.filter(user=request.user)

    if cid:
        Cart.objects.filter(id=cid, user=request.user).delete()
        request.session['cartitem'] = Cart.objects.filter(user=request.user).count()
        return HttpResponse("<script>alert('Item successfully removed');location.href='/cartitem/'</script>")

    return render(request, 'cartitem.html', {"cartdata": cartdata})


@login_required
def myorder(request):
    if request.user.user_type != 'customer':
        return HttpResponse("<script>alert('Only customers can place orders');location.href='/'</script>")
    msg = request.GET.get('msg')
    if msg:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            Myorders.objects.create(
                user=request.user,
                product_name=item.product_name,
                quantity=item.quantity,
                price=item.price,
                total_price=item.total_price,
                product_picture=item.product_picture,
                pw=item.pw,
                status="Pending",
                order_date=timezone.now().date(),
                
            )
        cart_items.delete()
        request.session['cartitem'] = 0
        return HttpResponse("<script>alert('Your order has been placed successfully!');location.href='/orderslist/'</script>")

    return render(request, 'order.html')


@login_required
def indexcart(request):
    if request.user.user_type != 'customer':
        return HttpResponse("<script>alert('Only customers can add items to cart');location.href='/'</script>")

    if request.GET.get('qt'):
        qt = int(request.GET.get('qt'))
        pname = request.GET.get('pname')
        ppic = request.GET.get('ppic')
        pw = request.GET.get('pw')
        price = int(request.GET.get('price'))
        total_price = qt * price

        if qt > 0:
            Cart.objects.create(
                user=request.user,
                product_name=pname,
                quantity=qt,
                price=price,
                total_price=total_price,
                product_picture=ppic,
                pw=pw,
                added_date=timezone.now().date()
            )
            request.session['cartitem'] = Cart.objects.filter(user=request.user).count()
            return HttpResponse("<script>alert('Your item was added in cart');location.href='/index/'</script>")
        else:
            return HttpResponse("<script>alert('Add product quantity to your cart');location.href='/index/'</script>")

    return render(request, 'indexcart.html')


@login_required
def orderslist(request):
    if request.user.user_type != 'customer':
        return HttpResponse("<script>alert('Only customers can view orders');location.href='/'</script>")

    oid = request.GET.get('oid')

    if oid:
        Myorders.objects.filter(id=oid, user=request.user).delete()
        return HttpResponse("<script>alert('Order canceled');location.href='/orderslist/'</script>")

    pdata = Myorders.objects.filter(user=request.user, status="Pending")
    adata = Myorders.objects.filter(user=request.user, status="Accepted")
    ddata = Myorders.objects.filter(user=request.user, status="Delivered")

    return render(request, 'orderlist.html', {
        "pdata": pdata,
        "adata": adata,
        "ddata": ddata
    })

# @login_required
# def place_order(request):
#     if request.user.user_type != 'customer':
#         return HttpResponse("<script>alert('Only customers can place orders');location.href='/'</script>")

#     if request.method == 'POST':
#         street = request.POST.get('street')
#         city = request.POST.get('city')
#         zip_code = request.POST.get('zip')

#         product_name = request.POST.get('product_name')
#         quantity = int(request.POST.get('quantity'))
#         quantity = request.POST.get('quantity')
#         price = float(request.POST.get('price'))
#         total_price = float(request.POST.get('total_price'))
#         product_picture = request.POST.get('product_picture')
#         pw = request.POST.get('pw')

#         full_address = f"{street}, {city}, {zip_code}"

#         Myorders.objects.create(
#             user=request.user,
#             product_name=product_name,
#             quantity=quantity,
#             price=price,
#             total_price=total_price,
#             product_picture=product_picture,
#             pw=pw,
#             order_date=timezone.now().date(),
#             status="Pending"
#         )

#         return HttpResponse("<script>alert('Order placed successfully!');location.href='/orderslist/'</script>")

#     # Pre-fill product data when GET request is sent
#     return render(request, 'address_form.html', {
#         'product_name': request.GET.get('product_name'),
#         'quantity': request.GET.get('quantity'),
#         'price': request.GET.get('price'),
#         'total_price': request.GET.get('total_price'),
#         'product_picture': request.GET.get('product_picture'),
#         'pw': request.GET.get('pw'),
#     })

@login_required
def delete_category(request, cid):
    category = get_object_or_404(Category, id=cid, seller=request.user)
    
    if request.user.user_type != 'seller':
        return HttpResponse("<script>alert('Unauthorized access');location.href='/'</script>")
    
    category.delete()
    return redirect('seller_dashboard')

