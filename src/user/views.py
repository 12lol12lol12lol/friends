from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from user.serializers import RegisterUserSerializer


class RegisterUserView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RegisterUserSerializer

# Create your views here.
