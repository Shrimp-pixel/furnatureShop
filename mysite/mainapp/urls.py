from django.urls import path, include
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.products, name='products'),
    path('category/<int:pk>/', views.products, name='category'),
    path('product/<int:pk>/', views.product, name='product'),

]
