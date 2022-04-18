import random

from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory
from basketapp.models import Basket


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return None


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_product(hot_product):
    return Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]


# Create your views here.
def index(request):
    context = {
        'products': Product.objects.all()[:4],
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    return render(request, 'mainapp/contact.html')


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()
    if pk is not None:
        if pk == 0:
            product_list = Product.objects.all()
            category_item = {
                'name': 'все',
                'pk': 0,
            }
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            product_list = Product.objects.filter(category__pk=pk)
        context = {
            'links_menu': links_menu,
            'title': 'Продукты',
            'product_list': product_list,
            'category_item': category_item,
            'basket': get_basket(request.user),
        }
        return render(request=request, template_name='mainapp/products_list.html', context=context)

    hot_product = get_hot_product()
    same_products = get_same_product(hot_product)
    context = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        'basket': get_basket(request.user),
    }
    return render(request=request, template_name='mainapp/products.html', context=context)


def product(request, pk):
    links_menu = ProductCategory.objects.all()
    context = {
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/product.html', context)
