from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import UserRegisterSerializer, UserProfileSerializer, ProfileCreateSerializer
from .models import Profile

# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code != 200:
            return Response({"success": False}, status=response.status_code)
        
        tokens = response.data
        access_token = tokens['access']
        refresh_token = tokens['refresh']

        # Set cookies directly on the same response object
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,      # HTTPS required for cross-domain
            samesite="None",  # must be None for cross-origin
            path="/",
            
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
            
        )

        response.data = {"success": True}
        return response
    

class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"refreshed": False}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Inject cookie token into request.data
        request.data['refresh'] = refresh_token
        response = super().post(request, *args, **kwargs)

        if response.status_code != 200:
            return Response({"refreshed": False}, status=response.status_code)

        access_token = response.data['access']
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
        )

        
        response.data = {"refreshed": True}
        return response
    
    
@api_view(['POST'])
@permission_classes([AllowAny])
def User_Register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': 'true'}, status=status.HTTP_201_CREATED)
    
    return Response({'success':'False'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def User_Logout(request):
    res = Response({'logout':'True'})
    res.delete_cookie('access_token', path='/')
    res.delete_cookie('refresh_token', path='/')
    return res

#----------Profile Endpoints-----------#

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Create_Profile(request):
    context = {"user": request.user}
    serializer = ProfileCreateSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        return Response({"Profile Creation": "True"}, status=status.HTTP_201_CREATED)
    return Response({"Profile Created": "False"}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def Profile_data(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "GET":
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


