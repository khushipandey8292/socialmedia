from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Category, Myproduct, CustomUser

@receiver(pre_delete, sender=Category)
def notify_sellers_on_category_delete(sender, instance, **kwargs):
    category = instance
    seller_ids = Myproduct.objects.filter(product_category=category).values_list('seller_id', flat=True).distinct() 
    sellers = CustomUser.objects.filter(id__in=seller_ids, user_type='seller')
    
    if not sellers.exists():
        print(f"No sellers found for category {category.cname}")
        return  
    
    for seller in sellers:
        if seller.email:
            print(f"Sending email to {seller.email} for category {category.cname}")
            subject = f"Category {category.cname} Deleted"
            message = f"Dear {seller.username}, the category {category.cname} has been deleted."
            from_email = settings.DEFAULT_FROM_EMAIL  
            recipient_list = [seller.email]
            
            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                print(f"Email successfully sent to {seller.email}")
            except Exception as e:
                print(f"Error sending email to {seller.email}: {e}")
        else:
            print(f"Seller {seller.username} does not have an email address.")
