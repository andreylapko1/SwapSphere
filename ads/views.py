from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.views import View
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView



class Login(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'ads/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.data)

        username = request.data.get('username')
        password = request.data.get('password')
        if form.is_valid():
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
        return render(request, 'ads/login.html', {'form': form})

class Register(View):
    permission_classes = (AllowAny,)
    def get(self, request):
        form = UserCreationForm()
        return render(request, "ads/register.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            response = redirect("/")
            return response
        else:
            return render(request, "ads/register.html", {"form": form})

# Create your views here.
