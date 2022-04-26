from django.urls import path
from . import views

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', views.user_create, name='user_create'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/update/<int:pk>/', views.user_update, name='user_update'),
    path('users/delete/<int:pk>/', views.user_delete, name='user_delete'),

    path('categories/create/', views.category_create, name='category_create'),
    path('categories/', views.categories, name='category_list'),
    path('categories/update/<int:pk>/', views.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),

    path('products/create/<int:pk>/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', views.ProductListView.as_view(), name='product_list'),
    path('products/update/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('products/detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

]
