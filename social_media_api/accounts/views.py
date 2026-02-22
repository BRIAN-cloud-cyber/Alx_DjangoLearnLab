
from rest_framework import generics,permissions,status
from .models import User
from .serializers import RegistrationSerializer , LoginSerializer , UserDetailSerializer
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    
class LoginView(ObtainAuthToken):
  serializer_class = LoginSerializer
  permission_classes = [permissions.AllowAny]

  def post(self,request):
     user=authenticate(username=request.data.get('username'), password=request.data.get('password'))
     if not user:
        return Response({'error':'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
     
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self ,request):
        user=request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'bio': user.bio,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,
            'followers_count': user.followers.count(),
            'following_count': user.following.count(),})