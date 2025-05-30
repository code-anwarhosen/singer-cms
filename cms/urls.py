from django.urls import path
from cms import views

urlpatterns = [
    path('', views.home, name='home'),
]
