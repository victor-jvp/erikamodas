import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from inventory.forms import CreateProductForm, EditProductForm, LocationForm, TransactionInlineFormset
from .models import Location, Product, TransactionDet, TransactionCab, TRANSACTION_TYPES
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
    
@login_required
def index(request):        
    products = Product.objects.all()    
    for product in products:
        if request.user.location is not None:
            stock = TransactionDet.objects.filter(location=request.user.location).aggregate(Sum('amount'))['amount__sum']
        else:
            stock = TransactionDet.objects.aggregate(Sum('amount'))['amount__sum']
        if stock is None:
            product.stock = 0.0
        else:
            product.stock = stock
        product.save()

    return render(
        request,
        'product_index.html',
        context={'products': products}
    )


@login_required
def details(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(
        request,
        'details.html',
        context={'product': product}
    )


@login_required
def edit(request, product_id):
    errors = None
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = EditProductForm(request.POST, instance=product)
        form.save()
        return redirect('product:index')

    return render(
        request,
        'product_edit.html',
        {
            'product': product,
            'errors': errors
        }
    )


def create_first_transaction(request, product):
    transaction_cab = TransactionCab.objects.create(
        date=datetime.datetime.now(),
        comment="Stock inicial",
        created_by=request.user)
    transaction_cab.save()
    transaction_det = TransactionDet.objects.create(
        cab=transaction_cab,
        type='E',  # Entrada
        location=request.user.location,
        product=product,
        amount=request.POST['stock']
    )
    transaction_det.save()

@login_required
def create(request):
    errors = None
    if request.method == 'POST':
        form = CreateProductForm(request.POST)
        if form.is_valid():
            new_product = form.save()
            create_first_transaction(request, product=new_product)
            return redirect('product:index')
        else:
            errors = form.errors.as_data()
    else:
        form = CreateProductForm()

    return render(
        request,
        'product_create.html',
        {
            'form': form,
            'errors': errors
        }
    )


@login_required
def ajax_transactions(request):
    # cab = TransactionCab.objects.all()
    
    if request.user.location is None:
        cab = TransactionCab.objects.all()
    else:
        cab = TransactionCab.objects.filter(
            details__location=request.user.location)
            
    data = []
    for item in cab:
        data.append({
            'id': item.id,
            'date': item.date.strftime("%d/%m/%Y"),
            'comment': item.comment,
            'details': list(item.details.values("product__name", "type", "location__name", "amount")),
        })
    return JsonResponse({ 'data': data, 'transaction_types': TRANSACTION_TYPES }, safe=False)


@login_required
def transaction_index(request):
    return render(
        request,
        'transaction_index.html'
    )
    

def update_stock():
    products = Product.objects.all()
    for product in products:
        stock = TransactionDet.objects.filter(product=product).aggregate(Sum('amount'))['amount__sum']
        product.stock = stock
        product.save()


@login_required
def transaction_create(request):
    errors = None
    formset = TransactionInlineFormset()
    
    if request.method == 'POST':
        try:
            transaction_cab = TransactionCab.objects.create(
                date=request.POST['date'],
                comment=request.POST['comment'],
                created_by=request.user)
            transaction_cab.save()
            formset = TransactionInlineFormset(request.POST, instance=transaction_cab)
            if formset.is_valid():
                formset.save()
                
                update_stock()
                
                resp = {
                    'title': 'Completado!',
                    'text': 'La transacción fue procesada correctamente',
                    'icon': 'success'
                }
            else:
                resp = {
                    'title': 'Aviso!',
                    'text': 'La transacción no es válida para procesar, verifique los campos e intente nuevamente.',
                    'icon': 'warning',
                    'errors': formset.errors
                }
        except Exception as ex:
            print(ex)
            resp = {
                'title': 'Error!',
                'text': 'Ha ocurrido un error en el proceso',
                'icon': 'error',
                'error': str(ex)
            }

        return JsonResponse(resp)
    else:
        
        locations = Location.objects.all()
        products = Product.objects.all()
        return render(
            request,
            'transaction_create.html',
            {
                'errors': errors,
                'context': {
                    'types': TRANSACTION_TYPES,
                    'locations': locations,
                    'products': products,
                    'formset': formset,
                }
            }
        )


# LOCATIONS

@login_required
def location_index(request):
    locations = Location.objects.all()

    return render(
        request,
        'location_index.html',
        context={'locations': locations}
    )


@login_required
def location_create(request):
    errors = None
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['locations'] = json.dumps(
                list(Location.objects.values('id', 'name')))
            return redirect('product:location_index')
        else:
            errors = form.errors.as_data()
    else:
        form = CreateProductForm()    
    
    return render(
        request,
        'location_create.html',
        {
            'form': form,
            'errors': errors,
        }
    )
    

@login_required
def location_edit(request, location_id):
    errors = None
    location = get_object_or_404(Location, id=location_id)

    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        form.save()
        request.session['locations'] = json.dumps(
            list(Location.objects.values('id', 'name')))
        return redirect('product:location_index')

    return render(
        request,
        'location_edit.html',
        {
            'location': location,
            'errors': errors
        }
    )
