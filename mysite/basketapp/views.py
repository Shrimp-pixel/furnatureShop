from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F
from django.template.loader import render_to_string
from django.urls import reverse

from .models import Basket
from mainapp.models import Product


# Create your views here.
@login_required
def basket(request):
    basket_items = Basket.objects.filter(user=request.user).select_related()

    context = {
        'basket_items': basket_items,
    }

    return render(request, 'basketapp/basket.html', context)


@login_required
def add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return redirect('mainapp:product', pk=pk)

    product_item = get_object_or_404(Product, pk=pk)

    basket_item = Basket.objects.filter(product=product_item, user=request.user).first()

    if not basket_item:
        basket_item = Basket(product=product_item, user=request.user)
        basket_item.quantity += 1
    else:
        basket_item.quantity = F('quantity') + 1

    basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, pk):
    basket_item = get_object_or_404(Basket, pk=pk)
    basket_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit(request, pk, quantity):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        quantity = int(quantity)
        basket_item = Basket.objects.get(pk=pk)

        if quantity > 0:
            basket_item.quantity = quantity
            basket_item.save()
        else:
            basket_item.delete()

        basket_list = Basket.objects.filter(user=request.user)

        context = {
            'basket_items': basket_list
        }

        result = render_to_string('basketapp/includes/inc_baskets_list.html', context)
        return JsonResponse({'result': result})

