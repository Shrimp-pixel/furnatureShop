from django.contrib.auth.decorators import user_passes_test
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.db.models import F
from django.db import connection

from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from .forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm, ProductCreateForm
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from mainapp.models import ProductCategory, Product


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)


class AccessMixin:

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# Create your views here.
@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()
            return redirect('adminapp:user_list')
    else:
        user_form = ShopUserRegisterForm()

    context = {
        'form': user_form,
    }
    return render(request, 'adminapp/user_form.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     context = {
#         'object_list': ShopUser.objects.all().order_by('-is_active')
#     }
#     return render(request, 'adminapp/users.html', context)


class UserListView(AccessMixin, ListView):
    template_name = 'adminapp/users.html'
    model = ShopUser
    ordering = '-is_active'



@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            return redirect('adminapp:user_list')
    else:
        user_form = ShopUserAdminEditForm(instance=current_user)

    context = {
        'form': user_form,
    }
    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        current_user.is_active = False if current_user.is_active else True
        current_user.save()
        return redirect('adminapp:user_list')

    context = {
        'object': current_user,
    }
    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    return None


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    context = {
        'object_list': ProductCategory.objects.all().order_by('-is_active')
    }
    return render(request, 'adminapp/categories.html', context)


#@user_passes_test(lambda u: u.is_superuser)
#def category_update(request):
#    return None

class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    template_name = 'adminapp/product_form.html'
    success_url = reverse_lazy('adminapp:category_list')

#   def get_success_url(self):
#       return reverse('adminapp:category_update', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data.get('discount')
            if discount:
                self.object.product_set.update(
                    price=F('price') * (1 - discount / 100.0)
                )
        return super().form_valid(form)

@user_passes_test(lambda u: u.is_superuser)
def category_delete(request):
    return None


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request):
#     return None

class ProductCreateView(AccessMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductCreateForm

    #    success_url = reverse_lazy('adminapp:product_list')

    def get_success_url(self):
        return reverse('adminapp:product_list', args=[self.kwargs['pk']])


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request):
#     return None

class ProductUpdateView(AccessMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     context = {
#         'object_list': Product.objects.filter(category__pk=pk).order_by('-is_active'),
#         'category': get_object_or_404(ProductCategory, pk=pk),
#     }
#     return render(request, 'adminapp/products.html', context)


class ProductListView(AccessMixin, ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return context_data

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk')).order_by('-is_active')


# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request):
#     return None


class ProductDeleteView(AccessMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


# @user_passes_test(lambda u: u.is_superuser)
# def product_detail(request):
#     return None


class ProductDetailView(AccessMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_detail.html'

