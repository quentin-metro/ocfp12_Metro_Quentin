# Generated by Django 4.2.1 on 2023-05-24 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='payement_due',
            new_name='payment_due',
        ),
    ]
