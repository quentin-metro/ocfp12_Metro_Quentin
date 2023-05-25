from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import redirect

from .models import Client, Contract, Event
from .permissions import IsSalesmen, IsManagermen, IsSupportmen
from .permissions import IsAssignedToClient, IsAssignedToContract, IsAssignedToEvent
from .serializers import UserSerializer, ClientSerializer, ContractSerializer, EventSerializer

"""@api_view(['POST'])
ne peut s'inscrire , doit etre creer par un gestionnaire
def signup_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.create(request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response("Invalid request", status=status.HTTP_400_BAD_REQUEST)"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def login_redirect(request):
    if request.user.groups.filter(name="Salesmen").exists():
        return redirect('clients')
    elif request.user.groups.filter(name="Supportmen").exists():
        return redirect('event')
    elif request.user.groups.filter(name="Managermen").exists():
        return redirect('admin')
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)



@api_view(['GET'])
@permission_classes([IsAuthenticated, (IsSalesmen or IsManagermen)])
def client_get_list(request):
    # GET list of client
    if request.method == 'GET':
        if request.user.groups.filter(name="Salesmen").exists():
            clients_list = Client.objects.filter(sales_contact=request.user).all()
        else:
            clients_list = Client.objects.all()
        if clients_list:
            serializer = ClientSerializer(clients_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, (IsSalesmen or IsManagermen)])
def client_create(request):
    # Create a new client
    if request.method == 'POST':
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
            augmented_serializer_data = serializer.data
            augmented_serializer_data['id'] = client.id
            return Response(augmented_serializer_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated, (IsAssignedToClient or IsManagermen)])
def client_handler(request, client_id):
    if Client.objects.filter(id=client_id).exists():
        # Get details of a specific client
        if request.method == 'GET':
            client = Client.objects.get(id=client_id)
            serializer = ClientSerializer(client)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Modify a new client
        if request.method == 'PUT':
            sales_contact = None
            # Allow modifying contact , only for manager
            if request.user.groups.filter(name="Salesmen").exists():
                sales_contact = request.user.id
            elif 'sales_contact' in request.form:
                sales_contact = request.data['sales_contact']
            data = {
                "id": client_id,
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
                client = serializer.edit(data)
                augmented_serializer_data = serializer.data
                augmented_serializer_data['id'] = client.id
                return Response(augmented_serializer_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, (IsAssignedToClient or IsManagermen)])
def client_convert(request, client_id):
    if Client.objects.filter(id=client_id).exists():
        client = Client.objects.get(id=client_id)
        serializer = ClientSerializer(client)
        serializer.convert()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, (IsAssignedToClient or IsManagermen)])
def client_get_contract_or_sign(request, client_id):
    if Client.objects.filter(id=client_id).exists():
        client = Client.objects.get(id=client_id)
        # GET list of contract of the clients
        if request.method == 'GET':
            contracts_list = Contract.objects.filter(client=client).all()
            if contracts_list:
                serializer = ContractSerializer(contracts_list, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({}, status=status.HTTP_200_OK)
        elif request.method == "POST":
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
@permission_classes([IsAuthenticated, (IsSalesmen or IsManagermen)])
def contract_get_list(request):
    # GET list of contracts
    if request.method == 'GET':
        if request.user.groups.filter(name="Salesmen").exists():
            contracts_list = Contract.objects.filter(sales_contact=request.user).all()
        else:
            contracts_list = Contract.objects.all()
        if contracts_list:
            serializer = ContractSerializer(contracts_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_200_OK)



@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated, (IsAssignedToContract or IsManagermen)])
def contract_handler(request, contract_id):
    if Contract.objects.filter(id=contract_id).exists():
        # Get details of a contract
        if request.method == 'GET':
            contract = Contract.objects.get(id=contract_id)
            serializer = ContractSerializer(contract)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Modify a contract
        if request.method == 'PUT':
            sales_contact = None
            # Allow modifying contact , only for manager
            if request.user.groups.filter(name="Salesmen").exists():
                sales_contact = request.user.id
            elif 'sales_contact' in request.form:
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
                contract = serializer.edit(data)
                serializer = ContractSerializer(contract)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, (IsAssignedToContract or IsManagermen)])
def contract_event(request, contract_id):
    if Contract.objects.filter(id=contract_id).exists():
        contract = Contract.objects.get(id=contract_id)
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
                serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated, (IsAssignedToContract or IsManagermen)])
def contract_client(request, contract_id):
    if Contract.objects.filter(id=contract_id).exists():
        # Get details of the client associated to this contract
        if request.method == 'GET':
            contract = Contract.objects.get(id=contract_id)
            client_id = contract.client.id
            client = Client.objects.get(id=client_id)
            serializer = ClientSerializer(client)
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, (IsSupportmen or IsManagermen)])
def event_get_list(request):
    # GET list of event
    if request.method == 'GET':
        if request.user.groups.filter(name="Supportmen").exists():
            events_list = Event.objects.filter(support_contact=request.user).all()
        else:
            events_list = Event.objects.all()
        if events_list:
            serializer = EventSerializer(events_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated, (IsAssignedToEvent or IsManagermen)])
def event_handler(request, event_id):
    if Event.objects.filter(id=event_id).exists():
        # Get details of an event
        if request.method == 'GET':
            event = Event.objects.get(id=event_id)
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Modify a event
        if request.method == 'PUT':
            support_contact = None
            # Allow modifying contact , only for manager
            if request.user.groups.filter(name="Supportmen").exists():
                support_contact = request.user.id
            elif 'support_contact' in request.form:
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
                event = serializer.edit(data)
                serializer = EventSerializer(event)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, (IsAssignedToEvent or IsManagermen)])
def event_end(request, event_id):
    if Event.objects.filter(id=event_id).exists():
        if request.method == 'POST':
            event = Event.objects.get(id=event_id)
            serializer = EventSerializer(event)
            event = serializer.end()
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, (IsAssignedToEvent or IsManagermen)])
def event_client(request, event_id):
    if Event.objects.filter(id=event_id).exists():
        # Get details of the client associated to this event
        if request.method == 'GET':
            event = Event.objects.get(id=event_id)
            client_id = event.client.id
            client = Client.objects.get(id=client_id)
            serializer = ClientSerializer(client)
            return Response(serializer.data, status=status.HTTP_200_OK)
