from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from inventory.forms import ProductForm, TransactionForm
from .models import Category, Product, Transaction, TransactionType
from django.contrib import messages


def index(request):
    products = Product.objects.all()

    return render(
        request,
        'product_index.html',
        context={'products': products}
    )


def details(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(
        request,
        'details.html',
        context={'product': product}
    )


def edit(request, product_id):
    errors = None
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'PUT':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/inventory')
        else:
            errors = form.errors.as_data()

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


def create(request):
    errors = None
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/inventory')
        else:
            errors = form.errors.as_data()
    else:
        form = ProductForm()

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


def ajax_transactions(request):
    transactions = Transaction.objects.values(
        'type', 'product', 'amount')
    data = {
        'data': list(transactions)
    }
    return JsonResponse(data)

def ajax_products_by_category(request):
    category_id = request.GET['category_id']
    if category_id:
        products = Product.objects.filter(category=category_id).values('id', 'name').order_by('name')
    else:
        products = []
    return JsonResponse(list(products), safe=False)


def transaction_index(request):
    return render(
        request,
        'transaction_index.html'
    )


def transaction_create(request):
    errors = None
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product:transactions_index')
        else:
            errors = form.errors.as_data()
    else:
        form = TransactionForm()

    categories = Category.objects.all().order_by('name')
    types = TransactionType.objects.values('id', 'name').order_by('order')

    return render(
        request,
        'transaction_create.html',
        {
            'form': form,
            'categories': categories,
            'errors': errors,
            'types': types
        }
    )