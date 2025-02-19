from django.contrib.auth import authenticate,get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Auth_Token
from rest_framework.authentication import get_authorization_header
from .serializer import RegistrationSerializer,LoginSerializer,ProfileSerializer
from .permissions import TokenAuthenticationPermission
from .models import Profile

# Create your views here.

User = get_user_model()

class RegistrationView(APIView):
    def post(self,request):
        serialzier = RegistrationSerializer(data=request.data)
        if serialzier.is_valid():
            serialzier.save()
            return Response({"Message":"User registered successfully."},status=status.HTTP_201_CREATED)
        else:
            return Response({"Message":"Enter valid data."},status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                token,created = Auth_Token.objects.get_or_create(user=user)
                return Response({"token":token.key},status=status.HTTP_200_OK)
            else:
                return Response({"error":"Invalid credentials."},status=status.HTTP_400_BAD_REQUEST)
    


class LogoutView(APIView):
    permission_classes = [TokenAuthenticationPermission] # this for check authentication befor log out
    def delete(self,request):
        token_key = self.get_token(request)

        if not token_key:
            return Response({"Token does not exists."},status=status.HTTP_400_BAD_REQUEST)
        try:
            token = Auth_Token.objects.get(key = token_key)
            token.delete() # this delete token and user can log out
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Auth_Token.DoesNotExist:
            return Response({"error":"Token Invalid."},status=status.HTTP_400_BAD_REQUEST)

    # this function create to get authetication token to logout user
    def get_token(self,request):
        auth_header = get_authorization_header(request).decode('utf-8')
        token_key = auth_header.split(' ')[1] if ' ' in auth_header else None
        return token_key

class ProfileView(APIView):
    permission_classes = [TokenAuthenticationPermission]
    def get(self,request):
        try:
            user = User.objects.get(username = request.user.username)
            user_profile = Profile.objects.get(user = user)
        except (User.DoesNotExist,Profile.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data,status=status.HTTP_200_OK)
    