import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from inventory.forms import CreateProductForm, EditProductForm, TransactionForm, TransactionInlineFormset
from .models import Location, Product, TransactionDet, TransactionCab, TransactionType
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Tipos de transacción
types = {
    'E': 'Entrada',
    'S': 'Salida',
    'A': 'Ajuste'
}
    
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
        comment="Stock inicial",
        created_by=request.user)
    transaction_cab.save()
    transaction_det = TransactionDet.objects.create(
        cab=transaction_cab,
        type=TransactionType.objects.get(id=1), # Entrada
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
    cab = TransactionCab.objects.all()
    data = []
    for item in cab:        
        data.append({
            'date': item.date.strftime("%d/%m/%Y"),
            'details': list(item.details.values("product__name", "type__name", "location__name", "amount")),
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
        types = TransactionType.objects.all()
        locations = Location.objects.all()
        products = Product.objects.all()
        return render(
            request,
            'transaction_create.html',
            {
                'errors': errors,
                'context': {
                    'types': types,
                    'locations': locations,
                    'products': products,
                    'formset': formset,
                }
            }
        )
