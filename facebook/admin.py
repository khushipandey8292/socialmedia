from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,UserOTP, Category,Myproduct,Subcategory,Cart,Myorders

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
class categoryAdmin(admin.ModelAdmin):
    list_display = ('id','seller','cname','cpic','cdate')

@admin.register(Subcategory)
class subcategoryAdmin(admin.ModelAdmin):
    list_display = ('id','category_name','subcategory_name')


@admin.register(Myproduct)
class myproductAdmin(admin.ModelAdmin):
    list_display = ('id','seller','product_category',
                    'subcategory_name', 'veg_name','price','discount_price',
                    'product_pic','total_discount','product_quantity','pdate')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id','user','product_name','quantity','price','total_price','product_picture','pw','added_date')


@admin.register(Myorders)
class MyordersAdmin(admin.ModelAdmin):
    list_display = ('id','user','product_name','quantity','price','total_price','product_picture','pw','status','order_date')

