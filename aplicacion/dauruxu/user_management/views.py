from django.shortcuts import render
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .forms import CreateUserForm, LoginUserForm
# Create your views here.


def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'user_management/register.html', context)


def login_page(request):
    form = LoginUserForm()
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            login(request, form.user_cache)

    context = {'form': form}
    return render(request, 'user_management/login.html', context)


def home(request):
    return render(request, 'user_management/dashboard.html')


def classification_models(request):
    return render(request, 'user_management/clasification_models.html')


def users(request):
    return render(request, 'user_management/users.html')
