import django_filters
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import Client, Contract, Event


class ClientFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        fields = ['company_name', 'email']

    def filtered(self):
        clients_list = self.queryset
        request = self.data
        if request:
            if 'email' in request.query_params:
                search = request.query_params['email']
                clients_list = clients_list.filter(email=search).all()

            if 'company_name' in request.query_params:
                search = request.query_params['company_name']
                clients_list = clients_list.filter(company_name=search).all()

            if 'search' in request.query_params:
                search = request.query_params['search']
                clients_list = clients_list.filter(
                    Q(company_name=search) | Q(email=search)
                ).all()
        return clients_list


class ContractFilter(django_filters.FilterSet):
    class Meta:
        model = Contract
        fields = ['payment_due', 'amount', 'client__company_name', 'client__email']

    def filtered(self):
        contracts_list = self.queryset
        request = self.data
        if request:
            if 'date' in request.query_params:
                search = request.query_params['date']
                try:
                    contracts_list = contracts_list.filter(payment_due=search).all()
                except ValidationError:
                    contracts_list = contracts_list.none()
            if 'amount' in request.query_params:
                search = request.query_params['amount']
                contracts_list = contracts_list.filter(amount=search).all()

            if 'email' in request.query_params:
                search = request.query_params['email']
                contracts_list = contracts_list.filter(client__email=search).all()

            if 'company_name' in request.query_params:
                search = request.query_params['company_name']
                contracts_list = contracts_list.filter(client__company_name=search).all()

            if 'search' in request.query_params:
                search = request.query_params['search']
                if isinstance(search, str):
                    try:
                        contracts_list = contracts_list.filter(amount=float(search)).all()
                    except ValueError:
                        try:
                            contracts_list = contracts_list.filter(payment_due=search).all()
                        except ValidationError:
                            contracts_list = contracts_list.filter(
                                Q(client__company_name=search) | Q(client__email=search)
                            ).all()
        return contracts_list


class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = ['date_event', 'client__company_name', 'client__email']

    def filtered(self):
        events_list = self.queryset
        request = self.data
        if request:
            if 'date' in request.query_params:
                search = request.query_params['date']
                try:
                    events_list = events_list.filter(date_event=search).all()
                except ValidationError:
                    events_list = events_list.filter.none().all()

            if 'email' in request.query_params:
                search = request.query_params['email']
                events_list = events_list.filter(client__email=search).all()

            if 'company_name' in request.query_params:
                search = request.query_params['company_name']
                events_list = events_list.filter(client__company_name=search).all()

            if 'search' in request.query_params:
                search = request.query_params['search']
                if isinstance(search, str):
                    try:
                        events_list = events_list.filter(date_event=search).all()
                    except ValidationError:
                        events_list = events_list.filter(
                            Q(client__company_name=search) | Q(client__email=search)
                        ).all()

        return events_list
