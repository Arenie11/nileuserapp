from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from . serializers import UserSerializer, ProfileSerializer, RegistrationSerializer
from . models import Profile
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login,logout
#registration
class RegistrationView(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('dashboard')
    def post (self, request):
        try:
           if request.user.is_authenticated:
               return Response({"message": "You are logged in already"})
           serializer= RegistrationSerializer(data= request.data)
           if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
        except Exception as e:
            return Response({'error': str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#login
class LoginView(APIView):
    permission_class= [IsAuthenticated]
    def post(self,request):
        try:
            username= request.data.get('username')
            password= request.data.get('password')
            user= authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({"Message": "user login successfully!"}, status= status.HTTP_200_OK)        
            return Response ({"Message": "username/password not correct"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#logout
class LogoutView(APIView):
    def post(self, request):
        try:
            logout(request)
            return Response({"Message": "user login successfully!"}, status= status.HTTP_200_OK)        
            
        except Exception as e:
            return Response({'error': str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#dashboard
class DashboardView(APIView):
    def get (self, request):
        try:
            user= request.user.profile
            return Response({"message": "welcome"+ " "+ user.fullname})
        except Exception as e:
            return Response({'error': str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)