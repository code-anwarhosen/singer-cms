from django.urls import path
from cms import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/fetch-accounts/', views.get_accounts),
]
