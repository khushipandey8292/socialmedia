from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('customer', 'Customer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_ROLES)
    is_verified = models.BooleanField(default=False)  
    def __str__(self):
        return f"{self.username} ({self.user_type})"


class UserOTP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)  # OTP stored as a string (6 digits)
    created_at = models.DateTimeField(auto_now_add=True)  # When OTP was generated

    def _str_(self):
        return f"{self.user.username} - {self.otp}"