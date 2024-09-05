from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('tenants/', views.tenants, name='tenants'),
    path('tenants_payment_filter/', views.tenants_payment_filter, name='tenants_payment_filter'),
    path('charges/', views.charges, name='charges'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]