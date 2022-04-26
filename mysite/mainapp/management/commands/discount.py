from datetime import timedelta

from django.db.models import Q, F, When, Case, IntegerField, DecimalField
from django.core.management.base import BaseCommand

from orderapp.models import OrderItem

from orderapp.models import Order


class Command(BaseCommand):

    def handle(self, *args, **options):
        action_1_discount = 0.3
        action_2_discount = 0.15
        action_3_discount = 0.05

        action_1_delta = timedelta(hours=12)
        action_2_delta = timedelta(days=1)

        action_1 = 1
        action_2 = 2
        action_3 = 3

        action_1_condition = Q(order__update_at__lte=F('order__created_at') + action_1_delta)

        action_2_condition = Q(Q(order__update_at__lte=F('order__created_at') + action_2_delta) &
                               Q(order__update_at__gt=F('order__created_at') + action_1_delta))

        action_3_condition = Q(order__update_at__gt=F('order__created_at') + action_2_delta)

        action_1_order = When(action_1_condition, then=action_1)
        action_2_order = When(action_2_condition, then=action_2)
        action_3_order = When(action_3_condition, then=action_3)

        action_1_price = When(action_1_condition, then=F('product__price') * F('quantity') * action_1_discount)
        action_2_price = When(action_2_condition, then=F('product__price') * F('quantity') * action_2_discount)
        action_3_price = When(action_3_condition, then=F('product__price') * F('quantity') * action_3_discount)

        is_send_to_procide = Q(order__status=Order.STATUS_SEND_TO_PROCEED)

        orders_items_list = OrderItem.objects.filter(is_send_to_procide).annotate(
            action_order=Case(
                action_1_order,
                action_2_order,
                action_3_order,
                output_field=IntegerField(),
            )
        ).annotate(
            total_price=Case(
                action_1_price,
                action_2_price,
                action_3_price,
                output_field=DecimalField(),
            )
        ).order_by('action_order')

        for item in orders_items_list:
            print(
                f'{item.action_order:3}: заказ №{item.order.pk:3}: {item.product.name:15}: {item.total_price:6.2f}: {item.order.update_at - item.order.created_at}')
