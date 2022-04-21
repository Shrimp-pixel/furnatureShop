import random

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Product, ProductCategory
from basketapp.models import Basket


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_product(hot_product):
    return Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]


# Create your views here.
def index(request):
    context = {
        'products': Product.objects.all()[:4],
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    return render(request, 'mainapp/contact.html')


class ProductsListView(ListView):
    model = Product
    template_name = 'mainapp/products_list.html'
    paginate_by = 2
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_pk = self.kwargs.get('pk')
        if category_pk != 0:
            queryset = queryset.filter(category__pk=category_pk)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        category_pk = self.kwargs.get('pk')
        context_data['links_menu'] = ProductCategory.objects.all()
        context_data['title'] = 'Продукты'
        if category_pk == 0:
            context_data['category'] = {
                'name': 'все',
                'pk': 0,
            }
        else:
            context_data['category'] = get_object_or_404(ProductCategory, pk=category_pk)
        return context_data


def products(request):
    links_menu = ProductCategory.objects.all()

    hot_product = get_hot_product()
    same_products = get_same_product(hot_product)
    context = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request=request, template_name='mainapp/products.html', context=context)


def product(request, pk):
    links_menu = ProductCategory.objects.all()
    context = {
        'product': get_object_or_404(Product, pk=pk),
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/product.html', context)
