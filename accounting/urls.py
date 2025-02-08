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
    path('edit_tenant/<int:id>', views.edit_tenant, name='edit_tenant'),
    path('delete_tenant/<int:id>', views.delete_tenant, name='delete_tenant'),
    path('change_apartment_tenant/', views.change_apartment_tenant, name='change_apartment_tenant'),
    path('change_phone_tenant/', views.change_phone_tenant, name='change_phone_tenant'),
    path('change_name_tenant/', views.change_name_tenant, name='change_name_tenant'),
    path('change_role_tenant/', views.change_role_tenant, name='change_role_tenant'),
    path('import_transactions/', views.import_transactions, name='import_transactions'),
    path('upload_transaction_history/', views.upload_transaction_history, name='upload_transaction_history'),
    path('transactions/', views.transactions, name='transactions'),
]