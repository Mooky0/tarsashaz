# Generated by Django 4.2.15 on 2024-09-03 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0004_tenant_type_alter_charge_paid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='charge',
            old_name='paid',
            new_name='status',
        ),
    ]
