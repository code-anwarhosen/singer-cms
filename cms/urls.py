from django.urls import path
from cms import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/get/<str:pk>/', views.get_account_details),
    
    path('home/fetch-accounts/', views.get_accounts),
    path('make-payment/<str:pk>/', views.create_payment),
    
    path('product/list/', views.product_list, name='products'),
    path('product/create/', views.create_product),
]
