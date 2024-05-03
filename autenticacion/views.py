from rest_framework.decorators import api_view #definir rutas de back
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404 #busca un obj en la bb para el login

# Para controlar la autenticación y los permisos en vistas y endpoints de API
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


@api_view(['POST'])
def login(request):
    
    user = get_object_or_404(User, username=request.data['username'])#validacion si existe ese user
    
    if not user.check_password(request.data['password']):
        return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, create = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    
    return Response({"token":token.key,"user": serializer.data},status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    
    #validacion si desde el front estan mandando la data correcta
    if serializer.is_valid():
        serializer.save()
    
        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()
        
        token = Token.objects.create(user=user)
        return Response({'token': token.key,"user": serializer.data},status=status.HTTP_201_CREATED )
    
    
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])#Pide un header con un token para poder validarlo 
@permission_classes([IsAuthenticated])#Para proteger la vista, tiene que estar autenticado 
def profile (request):
    
    print(request.user)
    return Response("You are login with {}".format(request.user.username),status=status.HTTP_200_OK)