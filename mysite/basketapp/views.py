from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import F
from .models import Basket
from mainapp.models import Product


# Create your views here.
def basket(request):
    basket_items = Basket.objects.filter(user=request.user)

    context = {
        'basket_items': basket_items,
    }

    return render(request, 'basketapp/basket.html', context)


def add(request, pk):
    product_item = get_object_or_404(Product, pk=pk)

    basket_item = Basket.objects.filter(product=product_item, user=request.user).first()

    if not basket_item:
        basket_item = Basket(product=product_item, user=request.user)
        basket_item.quantity += 1
    else:
        basket_item.quantity = F('quantity') + 1

    basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove(request, pk):
    basket_item = get_object_or_404(Basket, pk=pk)
    basket_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
