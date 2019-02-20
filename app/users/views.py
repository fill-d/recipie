from rest_framework import generics
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken

from users.serializers import UserSerializer, AuthTockenSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTockenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
