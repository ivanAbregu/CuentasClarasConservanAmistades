from rest_framework import serializers
from collections import defaultdict

from apps.order.models import Order, OrderByUser, Payment


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order

        fields = (
            "id",
        )
class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment

        fields = ("__all__")

class AccountSerializer(serializers.ModelSerializer):
    detail = serializers.SerializerMethodField(read_only=True)
    def get_detail(self, obj):
        d = defaultdict(list)
        for qs in obj.order_by_user.all():
            beer_detail = {
                "beer_name": qs.beer.name, 
                "beer_price": qs.beer.price, 
                "amount": qs.amount
            }
            d[qs.customer.username].append(beer_detail)
        return d


    class Meta:
        model = Order
        fields = ('id', "detail", "total", "is_paid")
