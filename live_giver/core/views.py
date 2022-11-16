from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Client
from .serializer import ClientSerializer, ClientCreationSerializer
from .verification import Verify

@api_view(['POST'])
def sign_up(request):
    user = request.data
    user.bvn = 54651333604

    if Verify().bvn_verification(number=user.bvn):
        # client = Client(name=user.name, phone_number=user.phone_number, email=user.email, bvn=user.bvn, password=user.password, location=user.location, age=user.age, weight=user.weight, blood_group=user.blood_group)
        # client.save()
        serializer = ClientCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'created'}, status=status.HTTP_201_CREATED)
        return Response({'message':'something is wrong with the data'})
    return Response({'message':'information wasnt verified'}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
def get_patients(request):

    if request.data.blood_group == 'O-':
        patient_filter = Client.objects.filter(needs_donation=True).all()
        serializer = ClientSerializer(patient_filter, many=True)
        return Response(serializer)
    patient_filter = Client.objects.filter(needs_donation=True, blood_group=request.data.blood_group).all()
    serializer = ClientSerializer(patient_filter, many=True)
    return Response(serializer) 

@api_view(['GET'])
def get_all_clients(request):
    
    patient_filter = Client.objects.all()
    serializer = ClientSerializer(patient_filter, many=True)
    return Response(serializer)
    


@api_view(['POST'])
def set_donation_status(request):
    client_info = dict(request.data)
    client = Client.objects.get(id=client_info.id)
    if client.eligible_donate():
        client.wants_to_donate= client_info.wants_to_donate
        client.save()
        return Response()
    else:
        return Response({"message": "Your are not eligible to donate yet"})


@api_view(['POST'])
def agree_to_donate(request):
    pass


@api_view(['POST'])
def set_patient_status(request):
    client_info = dict(request.data)
    client = Client.objects.get(id=client_info.id)
    client.wants_to_donate= client_info.wants_to_donate
    client.save()
    return Response()


@api_view(['GET'])
def home(request):
    return Response({'memmemmeme': 'Valid'})
    