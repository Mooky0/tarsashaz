import django.template.loader as loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .models import Charge, Payment, Expense, Tenant
from django.db.models import Sum

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
        'tenant' : Tenant.objects.get(email=str(request.user.email)),
    }
    return HttpResponse(template.render(context, request))
    
    
@login_required
def tenants(request):
    template = loader.get_template('accounting/tenants.html')
    tenants = Tenant.objects.all()
    
    
    context = {
        'tenants' : tenants,
        'tenant' : Tenant.objects.get(email=str(request.user.email))
    }
    
    return HttpResponse(template.render(context, request))
    
@login_required
def charges(request):
    template = loader.get_template('accounting/charges.html')
    tenants = Tenant.objects.all()
    
    context = {
       'tenants' : tenants,
        'tenant' : Tenant.objects.get(email=str(request.user.email)),
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
        'tenant' : Tenant.objects.get(email=str(user.email)),
    }
    
    return HttpResponse(template.render(context, request))
    
def home(request):
    return HttpResponse('Home page')

def about(request):
    return HttpResponse('About page')

def contact(request):    
    return HttpResponse('Contact page')

def profile(request):
    return HttpResponse('Profile page')

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