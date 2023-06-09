import logging
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import ClientFilter, ContractFilter, EventFilter
from .models import Client, Contract, Event
from .permissions import IsSalesmen, IsManagermen, IsSupportmen
from .permissions import IsAssignedToClient, IsAssignedToContract, IsAssignedToEvent
from .serializers import ClientSerializer, ContractSerializer, EventSerializer
# from .serializers import UserSerializer,

logger = logging.getLogger(__name__)

"""
@api_view(['POST'])
Can't signup , need to be created by a manager by admin site
def signup_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.create(request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response("Invalid request", status=status.HTTP_400_BAD_REQUEST)
"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def login_redirect(request):
    logger.info(f"\'{request.user}\' connected")
    if request.user.groups.filter(name="Salesmen").exists():
        return redirect('clients')
    elif request.user.groups.filter(name="Supportmen").exists():
        return redirect('events')
    elif request.user.groups.filter(name="Managermen").exists():
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)



@api_view(['GET'])
@permission_classes([IsAuthenticated, (IsSalesmen | IsManagermen)])
def client_get_list(request):
    # GET list of client
    if request.method == 'GET':
        logger.info(f"\'{request.user}\' GET client_get_list")
        if request.user.groups.filter(name="Salesmen").exists():
            clients_list = ClientFilter(request,
                                        queryset=Client.objects.filter(sales_contact=request.user).all()
                                        ).filtered()
        else:
            clients_list = ClientFilter(request,
                                        queryset=Client.objects.filter(sales_contact=request.user).all()
                                        ).filtered()
        if clients_list:
            serializer = ClientSerializer(clients_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, (IsSalesmen | IsManagermen)])
def client_create(request):
    # Create a new client
    if request.method == 'POST':
        logger.info(f"\'{request.user}\' POST client_create")
        sales_contact = None
        if request.user.groups.filter(name="Salesmen").exists():
            sales_contact = request.user.id
        data = {
            "company_name": request.data['company_name'],
            "email": request.data['email'],
            "phone": request.data['phone'],
            "mobile": request.data['mobile'],
            "first_name": request.data['first_name'],
            "last_name": request.data['last_name'],
            "isConverted": request.data['isConverted'],
            "sales_contact": sales_contact
        }
        serializer = ClientSerializer(data=data)
        if serializer.is_valid():
            client = serializer.create(data)
            serializer = ClientSerializer(client)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated, (IsAssignedToClient | IsManagermen)])
def client_handler(request, client_id):
    if Client.objects.filter(id=client_id).exists():
        client = Client.objects.get(id=client_id)
        # Get details of a specific client
        if request.method == 'GET':
            logger.info(f"\'{request.user}\' GET client_handler \'{client.company_name}\'")
            serializer = ClientSerializer(client)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Modify a new client
        if request.method == 'PUT':
            logger.info(f"\'{request.user}\' PUT client_handler  \'{client.company_name}\'")
            sales_contact = None
            sales_contact_change = False
            # Allow modifying contact , only for manager
            if request.user.groups.filter(name="Salesmen").exists():
                sales_contact = request.user.id
            elif 'sales_contact' in request.form:
                sales_contact_change = True
                sales_contact = request.data['sales_contact']
            data = {
                "id": client_id,
                "company_name": request.data['company_name'],
                "email": request.data['email'],
                "phone": request.data['phone'],
                "mobile": request.data['mobile'],
                "first_name": request.data['first_name'],
                "last_name": request.data['last_name'],
                "sales_contact": sales_contact
            }
            serializer = ClientSerializer(data=data)
            if serializer.is_valid():
                if sales_contact_change:
                    serializer.edit_contact(sales_contact)
                client = serializer.edit(data)
                serializer = ClientSerializer(client)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                logger.info(f"\'{request.user}\' PUT client_handler  \'{client.company_name}\' HTTP_406_NOT_ACCEPTABLE")
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, (IsAssignedToClient | IsManagermen)])
def client_convert(request, client_id):
    if Client.objects.filter(id=client_id).exists():
        client = Client.objects.get(id=client_id)
        logger.info(f"\'{request.user}\' POST client_convert \'{client.company_name}\' ")
        serializer = ClientSerializer(client)
        serializer.convert()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, (IsAssignedToClient | IsManagermen)])
def client_get_contract_or_sign(request, client_id):
    if Client.objects.filter(id=client_id).exists():
        client = Client.objects.get(id=client_id)
        # GET list of contract of the clients
        if request.method == 'GET':
            logger.info(f"\'{request.user}\' GET client_get_contract_or_sign \'{client.company_name}\' ")
            contracts_list = Contract.objects.filter(client=client).all()
            if contracts_list:
                serializer = ContractSerializer(contracts_list, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({}, status=status.HTTP_200_OK)
        elif request.method == "POST":
            logger.info(f"\'{request.user}\' POST client_get_contract_or_sign \'{client.company_name}\' ")
            if client.sales_contact is not None:
                data = {
                    'amount': request.data['amount'],
                    'payement_due': request.data['payment_due'],
                    'status': False,
                    'client': client.id,
                    'sales_contact': client.sales_contact.id
                }
                serializer = ContractSerializer(data=data)
                if serializer.is_valid():
                    contract = serializer.create(data)
                    serializer = ContractSerializer(contract)
                    logger.info(f"\'{request.user}\' POST client_get_contract_or_sign \'{contract.id}\' created")
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response(
                    {"Error": "This client doesn't have a assigned salesman"},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, (IsSalesmen | IsManagermen)])
def contract_get_list(request):
    # GET list of contracts
    if request.method == 'GET':
        logger.info(f"\'{request.user}\' GET contract_get_list")
        if request.user.groups.filter(name="Salesmen").exists():
            contracts_list = ContractFilter(request,
                                            queryset=Contract.objects.filter(sales_contact=request.user).all()
                                            ).filtered()
        else:
            contracts_list = ContractFilter(request,
                                            queryset=Contract.objects.all()
                                            ).filtered()
        if contracts_list:
            serializer = ContractSerializer(contracts_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_200_OK)



@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated, (IsAssignedToContract | IsManagermen)])
def contract_handler(request, contract_id):
    if Contract.objects.filter(id=contract_id).exists():
        contract = Contract.objects.get(id=contract_id)
        # Get details of a contract
        if request.method == 'GET':
            logger.info(f"\'{request.user}\' GET contract_handler \'{contract.id}\' ")
            serializer = ContractSerializer(contract)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Modify a contract
        if request.method == 'PUT':
            logger.info(f"\'{request.user}\' GET contract_handler \'{contract.id}\' ")
            sales_contact = None
            sales_contact_change = False
            # Allow modifying contact , only for manager
            if request.user.groups.filter(name="Salesmen").exists():
                sales_contact = request.user.id
            elif 'sales_contact' in request.form:
                sales_contact_change = True
                sales_contact = request.data['sales_contact']
            data = {
                "id": contract_id,
                "status": False,
                "amount": request.data['amount'],
                "payment_due": request.data['payment_due'],
                "sales_contact": sales_contact
            }
            serializer = ContractSerializer(data=data)
            if serializer.is_valid():
                if sales_contact_change:
                    serializer.edit_contact(sales_contact)
                contract = serializer.edit(data)
                serializer = ContractSerializer(contract)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, (IsAssignedToContract | IsManagermen)])
def contract_event(request, contract_id):
    if Contract.objects.filter(id=contract_id).exists():
        contract = Contract.objects.get(id=contract_id)
        logger.info(f"\'{request.user}\' POST contract_event \'{contract.id}\' ")
        if Event.objects.filter(contract=contract_id).exists():
            return Response(
                {"Error": "This contract already have a event"},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        else:
            data = {
                'attendees': request.data['attendees'],
                'date_event': request.data['date'],
                'notes': request.data['notes'],
                'status': False,
                'contract': contract.id,
                'client': contract.client.id,
                'support_contact': None
            }
            serializer = EventSerializer(data=data)
            if serializer.is_valid():
                event = serializer.create(data)
                logger.info(f"{request.user} POST contract_event \'{contract.id}\' created \'{event}\' ")
                serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated, (IsAssignedToContract | IsManagermen)])
def contract_client(request, contract_id):
    if Contract.objects.filter(id=contract_id).exists():
        # Get details of the client associated to this contract
        if request.method == 'GET':
            contract = Contract.objects.get(id=contract_id)
            logger.info(f"\'{request.user}\' GET contract_client \'{contract.id}\' ")
            client_id = contract.client.id
            client = Client.objects.get(id=client_id)
            serializer = ClientSerializer(client)
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, (IsSupportmen | IsManagermen)])
def event_get_list(request):
    # GET list of event
    if request.method == 'GET':
        logger.info(f"\'{request.user}\' GET event_get_list ")
        if request.user.groups.filter(name="Supportmen").exists():
            events_list = EventFilter(request,
                                      queryset=Event.objects.filter(support_contact=request.user).all()
                                      ).filtered()
        else:
            events_list = EventFilter(request.GET, queryset=Event.objects.all()).filtered()
        if events_list:
            serializer = EventSerializer(events_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated, (IsAssignedToEvent | IsManagermen)])
def event_handler(request, event_id):
    if Event.objects.filter(id=event_id).exists():
        event = Event.objects.get(id=event_id)
        # Get details of an event
        if request.method == 'GET':
            logger.info(f"\'{request.user}\' GET event_handler \'{event.id}\' ")
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Modify a event
        if request.method == 'PUT':
            logger.info(f"\'{request.user}\' PUT event_handler \'{event.id}\' ")
            support_contact = None
            support_contact_change = False
            # Allow modifying contact , only for manager
            if request.user.groups.filter(name="Supportmen").exists():
                support_contact = request.user.id
            elif 'support_contact' in request.form:
                support_contact_change = True
                support_contact = request.data['support']
            data = {
                'id': event_id,
                'attendees': request.data['attendees'],
                'date_event': request.data['date'],
                'notes': request.data['notes'],
                'status': False,
                'support_contact': support_contact
            }
            serializer = EventSerializer(data=data)
            if serializer.is_valid():
                if support_contact_change:
                    serializer.edit_contact(support_contact)
                event = serializer.edit(data)
                serializer = EventSerializer(event)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, (IsAssignedToEvent | IsManagermen)])
def event_end(request, event_id):
    if Event.objects.filter(id=event_id).exists():
        if request.method == 'POST':
            event = Event.objects.get(id=event_id)
            logger.info(f"\'{request.user}\' POST event_end \'{event.id}\' ended")
            serializer = EventSerializer(event)
            event = serializer.end()
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, (IsAssignedToEvent | IsManagermen)])
def event_client(request, event_id):
    if Event.objects.filter(id=event_id).exists():
        # Get details of the client associated to this event
        if request.method == 'GET':
            event = Event.objects.get(id=event_id)
            logger.info(f"\'{request.user}\' GET event_client \'{event}\' ")
            client_id = event.client.id
            client = Client.objects.get(id=client_id)
            serializer = ClientSerializer(client)
            return Response(serializer.data, status=status.HTTP_200_OK)
