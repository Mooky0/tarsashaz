from django.db import models

class Tenant(models.Model):
    class Role(models.TextChoices):
        TENANT = 'Tenant'
        LANDLORD = 'Landlord'
        PROPERTY_MANAGER = 'Property Manager'
    
    id = models.AutoField(primary_key=True)
    unit_number = models.CharField(max_length=10)
    tenant_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.TENANT)

    def __str__(self):
        return f'{self.unit_number} - {self.tenant_name}'


class Charge(models.Model):
    class PaymentStatus(models.TextChoices):
        PAID = 'Paid'
        PARTIALLY_PAID = 'Partially Paid'
        UNPAID = 'Unpaid'
    
    charge_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='charges')
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)


    def __str__(self):
        return f'Charge {self.description} for {self.tenant.tenant_name} status: {self.status}'


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    charge = models.ForeignKey(Charge, on_delete=models.CASCADE, related_name='payments')

    def __str__(self):
        return f'Payment of {self.amount_paid} for {self.charge.tenant.tenant_name}'

# Bank transactions for the account
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    hash = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    date = models.DateField()
    amount = models.IntegerField()
    bank_account = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255)
    bank_id = models.CharField(max_length=255)
    

class Expense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    paid_to = models.CharField(max_length=100)

    def __str__(self):
        return f'Expense {self.description} on {self.date}'