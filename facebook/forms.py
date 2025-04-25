from django import forms
from .models import Myproduct
from captcha.fields import CaptchaField

class OTPForm(forms.Form):
    otp = forms.CharField(
        label="Enter OTP",
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 6-digit OTP'})
    )
    
class Myform(forms.Form):
    captcha=CaptchaField()
  

class MyProductForm(forms.ModelForm):
    class Meta:
        model = Myproduct
        exclude = ['seller']


from .models import Category, Subcategory
from datetime import date

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['cname', 'cpic', 'cdate']  

    cdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = '__all__'

from django import forms

class AddressForm(forms.Form):
    full_name = forms.CharField(max_length=100, label='Full Name')
    phone = forms.CharField(max_length=15, label='Phone Number')
    address = forms.CharField(widget=forms.Textarea, label='Shipping Address')
    city = forms.CharField(max_length=50, label='City')
    postal_code = forms.CharField(max_length=10, label='Postal Code')
