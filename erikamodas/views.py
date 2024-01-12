from django.db import IntegrityError
from django.shortcuts import redirect, render
from inventory.forms import CustomUserCreationForm as UserCreationForm, CustomUserAuthenticationForm as AuthenticationForm
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from inventory.models import CustomUser as User
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

@login_required
def index(request):
    return render(request, 'index.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exist.'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password do not match.'
        })


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('home')


@login_required
def signout(request):
    logout(request)
    return redirect('signin')
