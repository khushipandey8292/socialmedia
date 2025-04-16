from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_otp_email(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP is: {otp}'
    from_email = 'khushipandey8292@gmail.com'  
    recipient_list = [email]
    sent = send_mail(subject, message, from_email, recipient_list)

    if sent == 0:
        raise Exception("Email not sent")
    return "OTP email sent successfully"
