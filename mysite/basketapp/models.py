from django.db import models

from django.conf import settings

from mainapp.models import Product


# Create your models here.
class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    add_datetime = models.DateTimeField(auto_now_add=True)

    @property
    def product_cost(self):
        return self.quantity * self.product.price

    @property
    def total_quantity(self):
        _items = self.user.basket.all()
        return sum(list(map(lambda x: x.quantity, _items)))

    @property
    def total_cost(self):
        _items = self.user.basket.all()
        return sum(list(map(lambda x: x.product_cost, _items)))