from django.urls import path
from . import views

app_name = 'basketapp'

urlpatterns = [
    path('', views.basket, name='basket'),
    path('add/<int:pk>/', views.add, name='add'),
    path('remove/<int:pk>/', views.remove, name='remove'),
    path('edit/<int:pk>/<int:quantity>/', views.edit, name='edit'),

]
