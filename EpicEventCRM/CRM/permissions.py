from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission

from .models import Client, Contract, Event


class IsSalesmen(BasePermission):
    message = "This user is not a salesmen."

    def has_permission(self, request, view):
        try:
            request.user.groups.get(name="Salesmen")
        except ObjectDoesNotExist:
            return False
        else:
            return True


class IsManagermen(BasePermission):
    message = "This user is not a managermen."

    def has_permission(self, request, view):
        try:
            request.user.groups.get(name="Managermen")
        except ObjectDoesNotExist:
            return False
        else:
            return True


class IsSupportmen(BasePermission):
    message = "This user is not a supportmen."

    def has_permission(self, request, view):
        try:
            request.user.groups.get(name="Supportmen")
        except ObjectDoesNotExist:
            return False
        else:
            return True


class IsAssignedToClient(BasePermission):
    message = "This user is not assigned to this client."

    def has_permission(self, request, view):
        client_id = view.kwargs['client_id']
        try:
            client = Client.objects.get(id=client_id)
        except ObjectDoesNotExist:
            return False
        else:
            if client.sales_contact == request.user:
                return True
            else:
                return False


class IsAssignedToContract(BasePermission):
    message = "This user is not assigned to this contract."

    def has_permission(self, request, view):
        contract_id = view.kwargs['contract_id']
        try:
            contract = Contract.objects.get(id=contract_id)
        except ObjectDoesNotExist:
            return False
        else:
            if contract.sales_contact == request.user:
                return True
            else:
                return False


class IsAssignedToEvent(BasePermission):
    message = "This user is not assigned to this event."

    def has_permission(self, request, view):
        event_id = view.kwargs['event_id']
        try:
            event = Event.objects.get(id=event_id)
        except ObjectDoesNotExist:
            return False
        else:
            if event.support_contact == request.user:
                return True
            else:
                return False
