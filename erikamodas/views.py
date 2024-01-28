from django.http import JsonResponse
from django.db import IntegrityError
from django.shortcuts import redirect, render
from inventory.forms import CustomUserCreationForm as UserCreationForm, CustomUserAuthenticationForm as AuthenticationForm
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from inventory.models import CustomUser as User, Location, Product, TransactionDet
from inventory.views import current_products
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
import json
from django.db.models import Sum

@login_required
def index(request):
    # Data for Products Chart
    data_products = []
    products = current_products(request)
    for product in products:
        data_products.append({"label": product.name, "y": product.stock})
    
    # Data for Locations Chart
    data_locations = []
    for location in Location.objects.all():
        data = []
        for product in products:
            stock = TransactionDet.objects.filter(location=location, product=product).aggregate(Sum('amount'))['amount__sum']
            if stock is None:
                stock = 0
            data.append({"label": product.name, "y": stock})
        data_locations.append({ 
            "type": "stackedBar100",
            "name": location.name,
            "dataPoints": data,
            "showInLegend": 1,
        })
        
    context = {
        "products": {
            "data": data_products,
            "title": "Inventario de Productos"
        },
        "locations": {
            "data": data_locations,
            "title": "Productos por Almacén"
        }
    }
    print(context)
    return render(request, 'index.html', {"context": context})


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
                request.session['locations'] = list(Location.objects.values('id', 'name'))
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
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'GET':
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
            request.session['locations'] = json.dumps(list(Location.objects.values('id', 'name')))
            return redirect('home')


@login_required
def signout(request):
    logout(request)
    return redirect('signin')


@login_required
def assign_location(request):
    location_id = request.GET['location_id']
    user = User.objects.get(pk=request.user.id)
    print(location_id)
    if location_id == "0":
        user.location = None
        user.save()
        return JsonResponse({'result': True}) 
        
    location = Location.objects.get(pk=location_id)
    if location is not None:
        user.location = location
        user.save()
        return JsonResponse({'result': True})
    else:
        return JsonResponse({'result': False})
