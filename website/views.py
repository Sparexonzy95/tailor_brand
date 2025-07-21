from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact, Collection, Testimonial, AboutImage  # Added AboutImage
from twilio.rest import Client
from decouple import config
import re
import logging

# Set up logging
logger = logging.getLogger(__name__)

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        request_type = request.POST.get('request-type')
        message = request.POST.get('message')

        # Validate form inputs
        if not name or len(name) < 2:
            messages.error(request, "Name must be at least 2 characters long.")
            return render(request, 'website/base.html', {
                'collections': Collection.objects.all(),
                'testimonials': Testimonial.objects.all(),
                'about_images': AboutImage.objects.all(),  # Added
                'about_values': ['Quality', 'Craftsmanship', 'Elegance'],  # Added
            })
        if not email and not phone:
            messages.error(request, "Email or phone is required.")
            return render(request, 'website/base.html', {
                'collections': Collection.objects.all(),
                'testimonials': Testimonial.objects.all(),
                'about_images': AboutImage.objects.all(),  # Added
                'about_values': ['Quality', 'Craftsmanship', 'Elegance'],  # Added
            })
        if not request_type in ['custom', 'alteration', 'consultation']:
            messages.error(request, "Invalid request type.")
            return render(request, 'website/base.html', {
                'collections': Collection.objects.all(),
                'testimonials': Testimonial.objects.all(),
                'about_images': AboutImage.objects.all(),  # Added
                'about_values': ['Quality', 'Craftsmanship', 'Elegance'],  # Added
            })
        if not message:
            messages.error(request, "Message is required.")
            return render(request, 'website/base.html', {
                'collections': Collection.objects.all(),
                'testimonials': Testimonial.objects.all(),
                'about_images': AboutImage.objects.all(),  # Added
                'about_values': ['Quality', 'Craftsmanship', 'Elegance'],  # Added
            })

        # Validate email format for auto-reply
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        is_email = email and re.match(email_regex, email)

        # Save to Contact model
        contact_instance = Contact(name=name, email=email or '', phone=phone or '', request_type=request_type, message=message)
        contact_instance.save()

        # Send auto-reply email (if email is provided and valid)
        if is_email:
            try:
                send_mail(
                    subject='Thank You for Contacting Bibiartisan',
                    message=f"Dear {name},\n\nThank you for your {request_type} request:\n\n{message}\n\nOur team will get back to you soon.\n\nBest,\nBibiartisan Team",
                    from_email='Bibiartisan <logicbloomlab@gmail.com>',
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, "Your inquiry has been submitted successfully! Check your email for a confirmation.")
            except Exception as e:
                logger.error(f"Failed to send auto-reply email: {str(e)}")
                messages.error(request, f"Failed to send confirmation email: {str(e)}")
        else:
            messages.success(request, "Your inquiry has been submitted successfully!")

        # Send email to brand
        try:
            contact_info = f"Email: {email or 'Not provided'}\nPhone: {phone or 'Not provided'}"
            send_mail(
                subject=f'New Contact Form Submission: {request_type}',
                message=f"Name: {name}\n{contact_info}\nRequest Type: {request_type}\nMessage: {message}",
                from_email='Bibiartisan <Bibiartisan.hub@gmail.com>',
                recipient_list=['Bibiartisan.hub@gmail.com'],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Failed to send brand email: {str(e)}")
            messages.error(request, f"Failed to notify brand: {str(e)}")

        # Send WhatsApp message to brand
        try:
            account_sid = config('TWILIO_ACCOUNT_SID')
            auth_token = config('TWILIO_AUTH_TOKEN')
            if not account_sid or not auth_token:
                raise ValueError("Twilio credentials are missing in environment variables.")
            logger.debug(f"Twilio Account SID: {account_sid}")
            client = Client(account_sid, auth_token)
            whatsapp_message = (
                f"*New Contact Form Submission*\n"
                f"*Name*: {name}\n"
                f"*Email*: {email or 'Not provided'}\n"
                f"*Phone*: {phone or 'Not provided'}\n"
                f"*Request Type*: {request_type}\n"
                f"*Message*: {message}"
            )
            client.messages.create(
                body=whatsapp_message,
                from_='whatsapp:+14155238886',
                to='whatsapp:+2349066026910',
            )
            logger.info("WhatsApp message sent successfully.")
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {str(e)}")
            messages.error(request, f"Failed to send WhatsApp message: {str(e)}")

        return redirect('home')

    # Optimize by fetching querysets once
    collections = Collection.objects.all()
    testimonials = Testimonial.objects.all()
    about_images = AboutImage.objects.all()  # Added
    about_values = ['Quality', 'Craftsmanship', 'Elegance']  # Added, can be from model if needed
    return render(request, 'website/base.html', {
        'collections': collections,
        'testimonials': testimonials,
        'about_images': about_images,
        'about_values': about_values
    })

def debug_env(request):
    return render(request, 'website/debug.html', {
        'twilio_account_sid': config('TWILIO_ACCOUNT_SID', default='Not Found'),
        'twilio_auth_token': config('TWILIO_AUTH_TOKEN', default='Not Found'),
        'email_host_user': config('EMAIL_HOST_USER', default='Not Found'),
        'email_host_password': config('EMAIL_HOST_PASSWORD', default='Not Found'),
    })