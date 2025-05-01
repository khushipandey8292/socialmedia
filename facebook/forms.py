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
        fields=['product_category','subcategory_name','veg_name','price','discount_price','product_pic','total_discount','product_quantity','pdate','stock']
        exclude = ['seller']
    pdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

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


class AddressForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), label="Address")
    city = forms.CharField(max_length=100, label="City")
    state = forms.CharField(max_length=100, label="State")
    zip_code = forms.CharField(max_length=10, label="Zip Code")
    phone_number = forms.CharField(max_length=15, label="Phone Number")

