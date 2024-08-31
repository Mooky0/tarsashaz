from django.contrib import admin

# Register your models here.

from .models import Charge, Payment, Expense, Tenant

admin.site.register(Charge)
admin.site.register(Payment)
admin.site.register(Expense)
admin.site.register(Tenant)