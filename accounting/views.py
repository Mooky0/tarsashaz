import django.template.loader as loader
from django.http import HttpResponse
from django.shortcuts import render

from .models import Charge, Payment, Expense, Tenant
from django.db.models import Sum


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
    }
    for expense in expenses:
        print(expense)
    return HttpResponse(template.render(context, request))
    
    
def tenants(request):
    template = loader.get_template('accounting/tenants.html')
    tenants = Tenant.objects.all()
    
    for tenant in tenants:
        print(tenant.tenant_name + ' ' + tenant.role)
    
    context = {
        'tenants' : tenants,
    }
    
    return HttpResponse(template.render(context, request))
    
def charges(request):
    template = loader.get_template('accounting/charges.html')
    tenants = Tenant.objects.all()
    
    context = {
        'tenants' : tenants,
    }
    
    return HttpResponse(template.render(context, request))
    
    
def tenants_payment_filter(request):
    tenants = Tenant.objects.all()
    payments = None
    tenant_id = request.GET.get('tenant')
    charges = Charge.objects.filter(tenant_id=tenant_id).order_by('amount')
    return render(request, 'partials/tenant_payments.html', {'charges': charges})

    
def home(request):
    return HttpResponse('Home page')

def about(request):
    return HttpResponse('About page')

def contact(request):    
    return HttpResponse('Contact page')