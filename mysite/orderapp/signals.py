from .models import OrderItem
from basketapp.models import Basket
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver


@receiver(pre_save, sender=Basket)
@receiver(pre_save, sender=OrderItem)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if instance.pk:
        instance.product.quantity -= instance.quantity - instance.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=Basket)
@receiver(pre_delete, sender=OrderItem)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()

