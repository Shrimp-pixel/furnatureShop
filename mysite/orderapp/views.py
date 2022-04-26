from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.forms.models import inlineformset_factory
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

from basketapp.models import Basket
from mainapp.models import Product
from .forms import OrderItemForm
from .models import Order, OrderItem


# Create your views here.
class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class OrderCreateView(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orderapp:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items.exists():
                OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=basket_items.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
            else:
                formset = OrderFormSet()
        context_data['orderitems'] = formset
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']
        with transaction.atomic():
            Basket.objects.filter(user=self.request.user).delete()
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderUpdateView(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orderapp:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
        context_data['orderitems'] = formset
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('orderapp:list')


class OrderDetailView(DetailView):
    model = Order


def order_forming_complete(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = Order.STATUS_SEND_TO_PROCEED
    order.save()
    return redirect('order:list')


def get_product_price(request, pk):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_item = Product.objects.filter(pk=pk).first()
        if product_item:
            return JsonResponse({'price': product_item.price})
        return JsonResponse({'price': 0})
