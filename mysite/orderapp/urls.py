from django.urls import path
from . import views


app_name = 'orderapp'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='list'),
    path('read/<pk>/', views.OrderDetailView.as_view(), name='read'),
    path('create/', views.OrderCreateView.as_view(), name='create'),
    path('update/<pk>/', views.OrderUpdateView.as_view(), name='update'),
    path('delete/<pk>/', views.OrderDeleteView.as_view(), name='delete'),
    path('cancel/forming/<pk>/', views.order_forming_complete, name='forming_cancel'),
    path('product/price/<int:pk>/', views.get_product_price, name='get_product_price'),
]
