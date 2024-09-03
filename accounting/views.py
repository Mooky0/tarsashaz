import django.template.loader as loader
from django.http import HttpResponse
from django.shortcuts import render

from .models import Charge, Payment, Expense, Tenant
from django.db.models import Sum


def index(request):
    template = loader.get_template('accounting/index.html')
    
    expanses = Expense.objects.aggregate(total=Sum('amount'))['total']
    
    payments = Payment.objects.aggregate(total=Sum('amount_paid'))['total']
    
    balance = payments - expanses
    
    
    context = {
        'total_balance' : "{:,.2f}".format(balance),
        'income' : "{:,.2f}".format(payments),
        'expense' : "{:,.2f}".format(expanses),
    }
    return HttpResponse(template.render(context, request))
    
    
def tenants(request):
    template = loader.get_template('accounting/tenants.html')
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