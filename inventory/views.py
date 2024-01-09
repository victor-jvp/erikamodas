import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from inventory.forms import CreateProductForm, EditProductForm, TransactionForm
from .models import Category, Product, Transaction, TransactionType, TransactionCab
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

    category = Category.objects.all().order_by('name')

    return render(
        request,
        'product_edit.html',
        {
            'product': product,
            'category': category,
            'errors': errors
        }
    )


@login_required
def create(request):
    errors = None
    if request.method == 'POST':
        form = CreateProductForm(request.POST)
        if form.is_valid():
            form.save()
            
            # transaction_cab = TransactionCab(
            #     date=datetime.datetime.now(),
            #     comment='Producto nuevo',
            #     created_by=request.user)
            # transaction_cab.save()
            
            # transaction_det = Transaction(
            #     cab_id=transaction_cab,
            #     type=TransactionType(pk=1),
            #     product=Product.objects.filter(pk=form.id),
            #     amount=request.POST['stock'])
            # transaction_det.save()
            
            return HttpResponseRedirect('/inventory')
        else:
            errors = form.errors.as_data()
    else:
        form = CreateProductForm()

    category = Category.objects.all().order_by('name')

    return render(
        request,
        'product_create.html',
        {
            'form': form,
            'category': category,
            'errors': errors
        }
    )


@login_required
def ajax_transactions(request):
    transactions = Transaction.objects.values(
        'type', 'product', 'amount')
    data = {
        'data': list(transactions)
    }
    return JsonResponse(data)


@login_required
def ajax_products_by_category(request):
    category_id = request.GET['category_id']
    if category_id:
        products = Product.objects.filter(category=category_id).values('id', 'name').order_by('name')
    else:
        products = []
    return JsonResponse(list(products), safe=False)


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
            
            transaction = TransactionForm(request.POST, instance=Transaction)
            print(transaction)
            transaction.cab_id = cab
                
            Transaction.objects.bulk_create(transaction).save()
            
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
        categories = Category.objects.all().order_by('name')
        types = TransactionType.objects.values('id', 'name').order_by('order')

        return render(
            request,
            'transaction_create.html',
            {
                'categories': categories,
                'errors': errors,
                'types': types
            }
        )