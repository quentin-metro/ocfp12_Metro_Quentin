from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import ModelSerializer

from .models import Client, Contract, Event


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username", 'first_name', 'last_name', 'email', 'password']

    def create(self, data):
        user = User.objects.create(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user.set_password(data['password'])
        user.save()
        return user



class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        read_only_fields = ['date_created']
        fields = ['id',
                  'company_name',
                  'email',
                  'phone',
                  'mobile',
                  'first_name',
                  'last_name',
                  'date_created',
                  'date_updated',
                  'isConverted',
                  'sales_contact'
                  ]

    def create(self, data):
        sales_contact = User.objects.get(id=data['sales_contact'])
        client = Client.objects.create(
            company_name=data['company_name'],
            email=data['email'],
            phone=data['phone'],
            mobile=data['mobile'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            isConverted=data['isConverted'],
            sales_contact=sales_contact
        )
        client.save()
        return client

    @staticmethod
    def edit(data):
        client = Client.objects.get(id=data['id'])
        client.id = client.id
        client.company_name = data['company_name']
        client.email = data['email']
        client.phone = data['phone']
        client.mobile = data['mobile']
        client.first_name = data['first_name']
        client.last_name = data['last_name']
        client.isConverted = client.isConverted
        client.date_updated = timezone.now()
        client.save()
        return client

    def convert(self):
        client_id = self.data['id']
        client = Client.objects.get(id=client_id)
        client.isConverted = True
        client.date_updated = timezone.now()
        client.save()
        return client


class ContractSerializer(ModelSerializer):
    class Meta:
        model = Contract
        read_only_fields = ['date_created']
        fields = ['id',
                  'status',
                  'amount',
                  'payment_due',
                  'date_created',
                  'date_updated',
                  'client',
                  'sales_contact'
                  ]

    def create(self, data):
        sales_contact = User.objects.get(id=data['sales_contact'])
        client = Client.objects.get(id=data['client'])
        contract = Contract.objects.create(
            status=data['status'],
            amount=data['amount'],
            payment_due=data['payment_due'],
            client=client,
            sales_contact=sales_contact
        )
        contract.save()
        return contract

    def edit(self, data):
        contract = Contract.objects.get(id=data['id'])
        contract.id = contract.id
        contract.amount = data['amount']
        contract.payment_due = data['payment_due']
        contract.date_updated = timezone.now()
        contract.save()
        return contract

    def end(self):
        # Finish the contract
        contract_id = self.data['id']
        contract = Contract.objects.get(id=contract_id)
        # Check if associated event are over
        try:
            Event.objects.get(contract=contract, status=True)
        except ObjectDoesNotExist:
            return False
        else:
            contract.id = contract.id
            contract.status = True
            contract.date_updated = timezone.now()
            contract.save()
            return contract


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        read_only_fields = ['date_created']
        fields = ['id',
                  'attendees',
                  'date_event',
                  'notes',
                  'status',
                  'date_created',
                  'date_updated',
                  'client',
                  'contract',
                  'support_contact'
                  ]

    def create(self, data):
        contract = Contract.objects.get(id=data['contract'])
        client = Client.objects.get(id=data['client'])
        event = Event.objects.create(
            attendees=data['attendees'],
            date_event=data['date_event'],
            notes=data['notes'],
            status=data['status'],
            contract=contract,
            client=client,
            support_contact=data['support_contact']
        )
        event.save()
        return event

    def edit(self, data):
        support_contact = User.objects.get(id=data['support_contact'])
        event = Event.objects.get(id=data['id'])
        event.id = event.id
        event.attendees = data['attendees']
        event.date_event = data['date_event']
        event.notes = data['notes']
        event.support_contact = support_contact
        event.date_updated = timezone.now()
        event.save()
        return event

    def end(self):
        # Finish the event
        event_id = self.data['id']
        event = Event.objects.get(id=event_id)
        event.id = event.id
        event.status = True
        event.date_updated = timezone.now()
        event.save()
        # Finish the associated contract
        if event.contract is not None:
            contract = Contract.objects.get(id=event.contract.id)
            ContractSerializer(contract).end()
        return event
