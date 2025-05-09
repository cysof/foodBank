from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile, User
from .serializers import UserSerializer, MyTokenObtainPairSerializer, ResterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .import serializers
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ResterSerializer


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'register': reverse('register', request=request),
        'login': reverse('login', request=request),
        'logout': reverse('logout', request=request),
        'token': reverse('token_obtain_pair', request=request),
        'token_refresh': reverse('token_refresh', request=request),
        'dashboard': reverse('dashboard', request=request),
    })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    if request.method == 'GET':
        response_message = f'Hey {request.user}, you are welcome on Board'
        return Response({'response': response_message}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        response_message = f'Hey {request.user}, you are welcome on Board'
        return Response({'response': response_message}, status=status.HTTP_200_OK)
    else:
        return Response({'response': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


# If you need user profile details
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    try:
        profile = user.profile
        data = {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'account_type': user.account_type,
            },
            'profile': {
                'profile_type': profile.profile_type,
                'bio': profile.bio,
                'date_of_birth': profile.date_of_birth,
                'residential_address': profile.residential_address,
                'bank_name': profile.bank_name,
                'account_number': profile.account_number,
            }
        }
        return Response(data, status=status.HTTP_200_OK)
    except:
        return Response({'detail': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    


def get_queryset(self):
    if not self.request.user.is_authenticated:
        return self.model.objects.none()  # Return empty queryset for anonymous users
    return super().get_queryset()