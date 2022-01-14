from .authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import exceptions 
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from core.models import User 

class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match') 
        data['is_ambassador'] = False 
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginAPIView(APIView):
    def post(self, request):
        data = request.data 

        email = data['email']
        password = data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Incorrect Password')


        token = JWTAuthentication.generate_jwt(user.id)

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'message': 'success'
        }
        return response


class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, _):
        response = Response()

        response.delete_cookie(key='jwt')

        response.data = {
            'message': 'logged out successfuly'
        }
        return response

class ProfileInfoAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user 

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ProfilePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user 
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match')
        
        user.set_password(data['password'])
        user.save()
        return Response(UserSerializer(user).data)

        



