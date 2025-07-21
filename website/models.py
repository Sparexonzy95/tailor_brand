from django.db import models
from cloudinary.models import CloudinaryField
from django.core.validators import FileExtensionValidator

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    request_type = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.request_type}"


class Collection(models.Model):
    category = models.CharField(max_length=50, unique=True)
    image = CloudinaryField('image', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category

    

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, help_text="Optional testimonial text or quote")
    video = CloudinaryField('video', resource_type='video', blank=True, null=True, help_text="Upload a video file (e.g., MP4)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - Testimonial"

class AboutImage(models.Model):
    image = CloudinaryField('image')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"About Image {self.order}"
