from django.urls import path
from .views import home, debug_env

urlpatterns = [
    path('', home, name='home'),
    path('debug/', debug_env, name='debug_env'),
]