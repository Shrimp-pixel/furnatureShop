from django.shortcuts import render
from .models import Product, ProductCategory


# Create your views here.
def index(request):
    context = {
        'products': Product.objects.all()[:4],
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    return render(request, 'mainapp/contact.html')


def products(request, pk=None):
    context = {
        'links_menu': ProductCategory.objects.all(),
    }
    return render(request=request, template_name='mainapp/products.html', context=context)


