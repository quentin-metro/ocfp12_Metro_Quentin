from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    company_name = models.fields.CharField(max_length=250, blank=True)
    email = models.fields.CharField(max_length=100, blank=True)
    phone = models.fields.CharField(max_length=20, blank=True)
    mobile = models.fields.CharField(max_length=20, blank=True)
    first_name = models.fields.CharField(max_length=25, blank=True)
    last_name = models.fields.CharField(max_length=25, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    isConverted = models.BooleanField(null=True)
    sales_contact = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.company_name


class Contract(models.Model):
    status = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField(auto_now_add=True, editable=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(to=Client, on_delete=models.SET_NULL, null=True)
    objects = models.Manager()


    def __str__(self):
        return str(self.pk)


class Event(models.Model):
    attendees = models.PositiveIntegerField()
    date_event = models.DateTimeField()
    notes = models.fields.TextField(max_length=2048, blank=True)
    status = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(to=Client, on_delete=models.SET_NULL, null=True)
    contract = models.ForeignKey(to=Contract, on_delete=models.SET_NULL, null=True)
    support_contact = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.pk)
