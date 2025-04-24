from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('customer', 'Customer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_ROLES)
    is_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)  
    def __str__(self):
        return f"{self.username}"

class UserOTP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)  
    created_at = models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
        return f"{self.user.username} - {self.otp}"
    
    @property
    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10) 

class Category(models.Model):
    cname=models.CharField(max_length=200,null=True)
    cpic=models.ImageField(upload_to='static/category/',null=True)
    cdate=models.DateField()
    def __str__(self):
        return  self.cname
    
class Subcategory(models.Model):
    category_name=models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory_name=models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.subcategory_name
    

class Myproduct(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    product_category=models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory_name=models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    veg_name=models.CharField(max_length=200,null=True)
    price=models.IntegerField()
    discount_price=models.IntegerField()
    product_pic=models.ImageField(upload_to='static/product/',null=True)
    total_discount=models.IntegerField()
    product_quantity=models.CharField(max_length=200)
    pdate=models.DateField()
    
class Cart(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=200)
    quantity=models.IntegerField(null=True)
    price=models.IntegerField(null=True)
    total_price=models.FloatField(null=True)
    product_picture=models.CharField(max_length=300,null=True)
    pw=models.CharField(max_length=200,null=True)
    added_date=models.DateField()
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity} for {self.user}"

class Myorders(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    quantity = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    total_price = models.FloatField(null=True)
    product_picture = models.CharField(max_length=300, null=True)
    pw = models.CharField(max_length=200, null=True)
    order_date = models.DateField(null=True)
    status=models.CharField(max_length=200,null=True,default="Pending")
    
    def __str__(self):
        return f"Order by {self.user} - {self.product_name} ({self.status})"



    
