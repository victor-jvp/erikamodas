from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from inventory.forms import ProductForm
from .models import Category, Product

# Create your views here.

# /productos


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


def create(request):
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
            'category' : category,
            'errors': errors
        }
    )
