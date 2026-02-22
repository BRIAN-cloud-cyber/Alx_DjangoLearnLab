
from rest_framework import generics
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
       user= serializer.save()
       Token.objects.create(user=user)

class LoginView(ObtainAuthToken):
    def post(self,request,*args,**kwargs):
        response=super().post(request,*args,**kwargs)
        token=response.data['token']
        user=Token.objects.get(key=token).user
        return Response({'token':token,'user_id':user.id,'username':user.username})