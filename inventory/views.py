import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from inventory.forms import CreateProductForm, EditProductForm, TransactionForm
from .models import Product, TransactionDet, TransactionCab
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    products = Product.objects.all()

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
        return HttpResponseRedirect('/inventory')

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
        location=request.user.location,
        comment="Stock inicial",
        created_by=request.user)
    transaction_cab.save()
    transaction_det = TransactionDet.objects.create(
        cab=transaction_cab,
        type="E",
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
            return HttpResponseRedirect('/inventory')
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
    transactions = TransactionDet.objects.all()
    data = []
    types = {
        'E': 'Entrada',
        'S': 'Salida',
        'A': 'Ajuste'
    }
    for item in transactions:
        data.append({
            'date': item.cab.date.strftime("%d/%m/%Y"),
            'type': types[item.type],
            'product': item.product.name,
            'amount': item.amount          
        })

    return JsonResponse({ 'data': data }, safe=False)


@login_required
def transaction_index(request):
    return render(
        request,
        'transaction_index.html'
    )


@login_required
def transaction_create(request):
    errors = None
    if request.method == 'POST':
        try:
            cab = TransactionCab(
                date=request.POST['date'],
                comment=request.POST['comment'],
                created_by=request.user
            ).save()

            transaction = TransactionForm(
                request.POST, instance=TransactionDet)
            print(transaction)
            transaction.cab = cab

            TransactionDet.objects.bulk_create(transaction).save()

            resp = {
                'title': 'Completado!',
                'text': 'La transacción fue procesada correctamente',
                'type': 'success'
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

        return render(
            request,
            'transaction_create.html',
            {
                'errors': errors,
            }
        )
