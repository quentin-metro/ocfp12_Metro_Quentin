# Generated by Django 4.2.1 on 2023-05-25 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0002_rename_payement_due_contract_payment_due'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='contract',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='CRM.contract'),
        ),
    ]
