from django.urls import path
from cms import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('home/fetch-accounts/', views.get_accounts),
    path('account/get/<str:pk>/', views.get_account_details),
    path('make-payment/<str:pk>/', views.create_payment),
    
    path('product/list/', views.product_list, name='products'),
    path('product/create/', views.create_product),
    
    path('account/create/', views.create_account, name='create-account'),
    path('account/precreation-data/', views.pre_creation_data),
    path('customer/create/', views.create_customer),
]
