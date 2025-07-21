from django.contrib import admin
from .models import Contact, Collection, Testimonial, AboutImage

@admin.register(AboutImage)
class AboutImageAdmin(admin.ModelAdmin):
    list_display = ['order', 'alt_text', 'created_at']
    list_editable = ['order', 'alt_text']
    list_filter = ['created_at']
    search_fields = ['alt_text']
    list_display_links = ['created_at']  # Fixes E124 and E123

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'request_type', 'created_at']
    list_filter = ['request_type', 'created_at']
    search_fields = ['name', 'email']

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['category', 'created_at']  # Changed 'name' to 'category'
    search_fields = ['category']  # Changed 'name' to 'category'
    list_display_links = ['category']  # Changed 'name' to 'category'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']