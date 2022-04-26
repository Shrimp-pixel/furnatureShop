import random

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.conf import settings
from django.core.cache import cache
from .models import Product, ProductCategory
from django.views.decorators.cache import cache_page


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'categories'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)

    return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category_item = cache.get(key)
        if category_item is None:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category_item)
        return category_item
    return get_object_or_404(ProductCategory, pk=pk)


def get_hot_product():
    try:
        return random.sample(list(Product.objects.all()), 1)[0]
    except:
        return None


def get_same_product(hot_product):
    return Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk).select_related()[:3]


# Create your views here.
def index(request):
    is_home = Q(category__name='дом')
    is_office = Q(category__name='офис')
    context = {
        'title': 'Главная',
        'products': Product.objects.filter(is_home | is_office),
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    return render(request, 'mainapp/contact.html')


class ProductsListView(ListView):
    model = Product
    template_name = 'mainapp/products_list.html'
    paginate_by = 2
    context_object_name = 'products'

    def _get_links_menu(self):
        return get_links_menu()

    def get_queryset(self):
        queryset = super().get_queryset()
        category_pk = self.kwargs.get('pk')
        if category_pk != 0:
            queryset = queryset.filter(category__pk=category_pk)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        category_pk = self.kwargs.get('pk')
        context_data['links_menu'] = self._get_links_menu()
        context_data['title'] = 'Продукты'
        if category_pk == 0:
            context_data['category'] = {
                'name': 'все',
                'pk': 0,
            }
        else:
            context_data['category'] = get_category(category_pk)
        return context_data


#@cache_page(3600)
def products(request):
    links_menu = get_links_menu()

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
    links_menu = get_links_menu()
    context = {
        'product': get_object_or_404(Product, pk=pk),
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/product.html', context)
