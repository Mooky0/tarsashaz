import django.template.loader as loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from django.contrib.auth.models import User
from .models import Charge, Payment, Expense, Tenant, Transaction
from django.db.models import Sum

import pandas as pd
import os
from datetime import datetime
import hashlib

@login_required
def index(request):
    template = loader.get_template('accounting/index.html')
    
    expanses_total = Expense.objects.aggregate(total=Sum('amount'))['total']
    
    payments = Payment.objects.aggregate(total=Sum('amount_paid'))['total']
    
    balance = payments - expanses_total
    
    expenses = Expense.objects.all()
    
    
    context = {
        'total_balance' : "{:,.2f}".format(balance),
        'income' : "{:,.2f}".format(payments),
        'expense' : "{:,.2f}".format(expanses_total),
        'expenses' : expenses,
        'user' : Tenant.objects.get(email=str(request.user.email)),
    }
    return HttpResponse(template.render(context, request))
    
    
@login_required
def tenants(request):
    template = loader.get_template('accounting/tenants.html')
    tenants = Tenant.objects.all()
    
    
    context = {
        'tenants' : tenants,
        'user' : Tenant.objects.get(email=str(request.user.email))
    }
    
    return HttpResponse(template.render(context, request))
    
@login_required
def charges(request):
    template = loader.get_template('accounting/charges.html')
    tenants = Tenant.objects.all()
    
    context = {
       'tenants' : tenants,
        'user' : Tenant.objects.get(email=str(request.user.email)),
    }
    
    return HttpResponse(template.render(context, request))
    
    
@login_required
def tenants_payment_filter(request):
    tenant = Tenant.objects.get(email=request.user.email)
    if tenant.role != 'Property Manager':
        return HttpResponse('You are not a tenant')
    tenants = Tenant.objects.all()
    payments = None
    tenant_id = request.GET.get('tenant')
    charges = Charge.objects.filter(tenant_id=tenant_id).order_by('amount')
    return render(request, 'partials/tenant_payments.html', {'charges': charges})

@login_required
def my_charges(request):
    user = request.user
    print(user.email)
    try:
        tenant = Tenant.objects.get(email=str(user.email))
    except Tenant.DoesNotExist:
        return HttpResponse('Tenant not found')
    template = loader.get_template('accounting/my_charges.html')
    charges = Charge.objects.filter(tenant_id=tenant.id)
    
    context = {
        'charges' : charges,
        'user' : Tenant.objects.get(email=str(user.email)),
    }
    
    return HttpResponse(template.render(context, request))
   
@login_required 
def add_tenant(request):
    tenant = Tenant.objects.get(email=request.user.email)
    if tenant.role != 'Property Manager':
        return HttpResponseRedirect(reverse('index')) 

    roles_raw = Tenant.Role.choices
    roles = []
    for role in roles_raw:
        roles.append(role[1])
        
    context = {
        'roles' : roles,
        'user' : tenant,
    }
    return render(request, 'accounting/add_tenant.html', context) 

@login_required    
def add_tenant_action(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('add_tenant'))
    tenant = Tenant.objects.get(email=request.user.email)
    if tenant.role != 'Property Manager':
        return HttpResponseRedirect(reverse('index'))
    
    name = request.POST['name']
    apt_number = request.POST['apartment']
    email = request.POST['email']
    phone_number = request.POST['phone']
    role = request.POST['role']
    user = User.objects.create_user(email, email, 'password') 
    user.save()
    tenant = Tenant(tenant_name = name, unit_number=apt_number, email=email, phone_number=phone_number, role=role)
    tenant.save()
    return HttpResponseRedirect(reverse('tenants'))

@login_required
def profile(request):
    tenant = Tenant.objects.get(email=request.user.email)
    context = {
        'tenant' : tenant,
        'user' : tenant,
    }
    return render(request, 'accounting/profile.html', context)

@login_required
def change_name(request):
    tenant = Tenant.objects.get(email=request.user.email)
    tenant.tenant_name = request.POST['name']
    tenant.save()
    return HttpResponse(render(request, 'partials/change_name.html', {'tenant': tenant}))

@login_required
def change_apartment(request):
    tenant = Tenant.objects.get(email=request.user.email)
    tenant.unit_number = request.POST['apartment']
    tenant.save()
    return HttpResponse(render(request, 'partials/change_apartment.html', {'tenant': tenant}))

@login_required
def change_phone(request):
    tenant = Tenant.objects.get(email=request.user.email)
    tenant.phone_number = request.POST['phone']
    tenant.save()
    return HttpResponse(render(request, 'partials/change_phone.html', {'tenant': tenant}))

@login_required
def change_email(request):
    new_email = request.POST['email']
    tenant = Tenant.objects.get(email=request.user.email)
    tenant.email = new_email
    tenant.save()
    ## FIXME fix this, it should update the email in the User table
    ## but it is not working. 
    User.objects.filter(email=tenant.email).update(username=new_email)
    User.objects.filter(email=tenant.email).update(email=new_email)
    return HttpResponse(render(request, 'partials/change_email.html', {'tenant': tenant}))

@login_required
def delete_tenant(request):
    tenant = Tenant.objects.get(email=request.user.email)
    if tenant.role != 'Property Manager':
        return HttpResponseRedirect(reverse('index'))
    tenant.delete()
    return HttpResponse(render(request, 'partials/tenant_table.html', {'tenant': tenant}))

@login_required
def edit_tenant(request, id):
    tenant = Tenant.objects.get(email=request.user.email)
    if tenant.role != 'Property Manager':
        return HttpResponseRedirect(reverse('index')) 

    edit_tenant = get_object_or_404(Tenant, pk=id)
    roles_raw = Tenant.Role.choices
    roles = []
    for role in roles_raw:
        roles.append(role[1])
    context = {
        'tenant' : edit_tenant,
        'user' : tenant,
        'roles' : roles,
    }
    return HttpResponse(render(request, 'accounting/edit_tenant.html', context))

@login_required
def delete_tenant(request, id):
    logged_in_user = Tenant.objects.get(email=request.user.email)
    if logged_in_user.role != 'Property Manager':
        return HttpResponseRedirect(reverse('index'))
    
    tenant = Tenant.objects.get(id=id)
    tenant.delete()
    return HttpResponseRedirect(reverse('tenants'))

@login_required
def change_apartment_tenant(request):
    user = Tenant.objects.get(email=request.user.email)
    if user.role != 'Property Manager':
        return HttpResponseRedirect(reverse('index'))
    new_apt = request.POST['apartment']
    tenant_id = request.POST['tenant_id']
    print("Tenant ID: ", tenant_id, "New Apartment: ", new_apt)
    tenant = Tenant.objects.get(id=tenant_id)
    tenant.unit_number = new_apt
    tenant.save()
    return HttpResponse(render(request, 'partials/change_apartment_tenant.html', {'tenant': tenant, 'user': user}))
    
    
@login_required
def change_phone_tenant(request):
    user = Tenant.objects.get(email=request.user.email)
    if user.role != 'Property Manager':
        return HttpResponseRedirect(reverse('index'))
    new_phone = request.POST['phone']
    tenant_id = request.POST['tenant_id']
    tenant = Tenant.objects.get(id=tenant_id)
    tenant.phone_number = new_phone
    tenant.save()
    return HttpResponse(render(request, 'partials/change_phone_tenant.html', {'tenant': tenant, 'user': user}))

@login_required
def change_name_tenant(request):
    user = Tenant.objects.get(email=request.user.email)
    if user.role != 'Property Manager':
        return HttpResponseRedirect(reverse('index'))
    new_name = request.POST['name']
    tenant_id = request.POST['tenant_id']
    tenant = Tenant.objects.get(id=tenant_id)
    tenant.tenant_name = new_name
    tenant.save()
    return HttpResponse(render(request, 'partials/change_name_tenant.html', {'tenant': tenant, 'user': user}))

@login_required
def change_role_tenant(request):
    user = Tenant.objects.get(email=request.user.email)
    if user.role != 'Property Manager':
        return HttpResponseRedirect(reverse('index'))
    new_role = request.POST['role']
    tenant_id = request.POST['tenant_id']
    tenant = Tenant.objects.get(id=tenant_id)
    tenant.role = new_role
    tenant.save()
    roles_raw = Tenant.Role.choices
    roles = []
    for role in roles_raw:
        roles.append(role[1])
    return HttpResponse(render(request, 'partials/change_role_tenant.html', {'tenant': tenant, 'user': user, 'roles': roles}))

@login_required
def import_transactions(request):
    tenant = Tenant.objects.get(email=request.user.email)
    if tenant.role != 'Property Manager':
        return HttpResponseRedirect(reverse('index'))
    context = {
        'user' : Tenant.objects.get(email=str(request.user.email)),
    }
    return render(request, 'accounting/import_transactions.html', context)

@login_required
def upload_transaction_history(request):
    tenant = Tenant.objects.get(email=request.user.email)
    if tenant.role != 'Property Manager':
        return HttpResponseRedirect(reverse('index'))

    print(request.FILES)

    if 'docfile' not in request.FILES:
        return HttpResponse("No file uploaded", status=400)

    transaction_file = request.FILES['docfile']
    file_path = "/tmp/files/transaction_history_{}.html".format(str(datetime.now))  # Ensure correct extension
    print(transaction_file.content_type) 

    # Save the uploaded file
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb+') as destination:
        for chunk in transaction_file.chunks():
            destination.write(chunk)

    # Read the saved file using pandas
    try:
        df = pd.read_html(file_path)
        df = df[2].reset_index()
        for index, row in df.iterrows():
            hashed = hashlib.sha256(str(row).encode()).hexdigest()
            if Transaction.objects.filter(hash=hashed).exists():
                continue
            date = datetime.strptime(row['Tranzakció időpontja'], '%Y.%m.%d. %H:%M:%S')
            transaction = Transaction(
                hash=hashed,
                type=row['Forgalom típusa'],
                date=date,
                amount=row['Összeg'],
                bank_account=row['Ellenoldali számlaszám'],
                name=row['Ellenoldali név'],
                description=row['Közlemény'],
                bank_id=row['Banki tranzakció azonosító']
            )
            transaction.save()
    except Exception as e:
        return HttpResponse(f"Error reading Excel file: {str(e)}", status=400)

    return HttpResponseRedirect(reverse('index'))

def transactions(request):
    tenant = Tenant.objects.get(email=request.user.email)
    if tenant.role != 'Property Manager':
        return HttpResponseRedirect(reverse('index'))
    transactions = Transaction.objects.all()
    context = {
        'transactions' : transactions,
        'transaction_cnt': len(transactions), 
        'user' : Tenant.objects.get(email=str(request.user.email)),
    }
    return render(request, 'accounting/transactions.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index')
    return render(request, 'accounting/login.html') 

def login_action(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        print('Login successful')
        return HttpResponseRedirect(reverse('index')) 
    print('Login failed')
    return HttpResponseRedirect(reverse('login'))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))