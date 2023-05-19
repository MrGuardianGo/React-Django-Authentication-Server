import datetime

from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer
from .models import User, UserToken
from .authentication import create_access_token, create_refresh_token, decode_access_token


class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Login(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid credentials')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Invalid credentials')

        refresh_token = create_refresh_token(user.id)
        access_token = create_access_token(user.id)

        UserToken.objects.create(
            user_id=user.id,
            token=refresh_token,
            expired_at=datetime.datetime.utcnow() + datetime.timedelta(days=365)
        )

        response = Response()

        response.set_cookie(key='refresh_token',
                            value=refresh_token, samesite='None', secure=True)
        response.set_cookie(key='access_token',
                            value=access_token, samesite='None', secure=True)
        response.data = UserSerializer(user).data
        return response

class GetUser(APIView):
    def get(self, request):
        token = request.COOKIES.get('access_token')
        user_id = decode_access_token(token)
        user = User.objects.filter(id=user_id).first()

        if user is None:
            raise exceptions.AuthenticationFailed('unauthenticated')

        return Response(UserSerializer(user).data)
