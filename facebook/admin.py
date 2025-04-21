from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,UserOTP,Category,Subcategory,Myproduct

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id','username', 'email', 'user_type', 'is_verified', 'is_staff', 'is_superuser')
    list_filter = ('user_type', 'is_verified', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('user_type', 'is_verified', 'phone', 'address')}),
    )
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(UserOTP)
class UserOTPAdmin(admin.ModelAdmin):
    list_display=['id','user','otp','created_at']
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','cname','cpic','cdate')

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id','category_name','subcategory_name')

@admin.register(Myproduct)
class MyproductAdmin(admin.ModelAdmin):
    list_display = ('id','product_category',
                    'subcategory_name', 'veg_name','price','discount_price',
                    'product_pic','total_discount','product_quantity','pdate');

