from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tenants/', views.tenants, name='tenants'),
    path('tenants_payment_filter/', views.tenants_payment_filter, name='tenants_payment_filter'),
    path('charges/', views.charges, name='charges'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('login_action/', views.login_action, name='login_action'),
    path('logout/', views.logout_view, name='logout'),
    path('my_charges/', views.my_charges, name='my_charges'),
    path('add_tenant/', views.add_tenant, name='add_tenant'),
    path('add_tenant_action/', views.add_tenant_action, name='add_tenant_action'),
    path('change_name/', views.change_name, name='change_name'),
    path('change_apartment/', views.change_apartment, name='change_apartment'),
    path('change_phone/', views.change_phone, name='change_phone'),
    path('change_email/', views.change_email, name='change_email'),
]