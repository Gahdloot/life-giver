from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Client
from .serializer import ClientSerializer, ClientCreationSerializer
from .verification import Verify

@api_view(['POST'])
def sign_up(request):

    #user = request.data(mutable=True)
    user = request.data.copy()
    user.update({'bvn':54651333604})
    user.update({'age':29})
    user.update({'weight':140})
    user['bvn'] = 54651333604

    if Verify().bvn_verification(number=user['bvn']):
        # client = Client(name=user.name, phone_number=user.phone_number, email=user.email, bvn=user.bvn, password=user.password, location=user.location, age=user.age, weight=user.weight, blood_group=user.blood_group)
        # client.save()
        user['bvn'] = 2147483647
        serializer = ClientCreationSerializer(data=user)
        print(type(user['weight']))
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'created'}, status=status.HTTP_201_CREATED)
        return Response({'message':'something is wrong with the data'})
    return Response({'message':'information wasnt verified'}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
def login(request):
    
    if request.data['email']:
        try:
            user = Client.objects.get(email=request.data['email'])
        except Client.DoesNotExist:
            return Response({'message':'This User doesnot exist, please check email'}, status=status.HTTP_404_NOT_FOUND)
        if request.data['password'] == user.password:
            return Response({'message':'successfully logged in'}, status=status.HTTP_202_ACCEPTED)
        return Response({'message': 'password does not match'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    return Response({'message': 'email field is blank'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_patients(request):

    if request.data['blood_group'] == 'O-':
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
    client_info = request.data
    client = Client.objects.get(id=client_info['id'])
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
    return Response({'message': 'This is the home page for the Blood donation app'})
    