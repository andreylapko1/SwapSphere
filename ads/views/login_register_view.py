from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.views import View
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView



from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from ads.serializers.login_serializer import LoginSerializer


class Login(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user is not None:
            login(request, user)
            return Response({'success': 'Вы вошли в систему'}, status=status.HTTP_200_OK)
        return Response({'error': 'Неверный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)






class Register(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        form = UserCreationForm()
        return render(request, "ads/register.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            response = redirect("/api")
            return response
        else:
            return render(request, "ads/register.html", {"form": form})

# Create your views here.
