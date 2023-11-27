from collections import defaultdict

from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from apps.order.models import Order, OrderByUser, Payment
from apps.beer.models import Beer
from .serializers import OrderSerializer, AccountSerializer, PaymentSerializer

from django.contrib.auth import get_user_model

User = get_user_model()

class OrderViewSet(ModelViewSet):
    """
        retrieve:
        Return the given Order.

        list:
        Return a list of all the existing Orders.

        create:
        Create a new Order. Recieve as param a dic of usename with a dic of beers wih the amount
        example: {"ivan": {"red":4, "ipa":3},"pedro": {"blonde":1}}

        update:
        Update a Order instance
    """

    queryset = Order.objects.all().order_by("-created")
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        data = self.request.data
        for username, values in data.items():
            user, _ = User.objects.get_or_create(username=username)
            for beer_name, amount in values.items():
                beer, _ = Beer.objects.get_or_create(name=beer_name)
                OrderByUser.objects.create(order=order, customer=user, beer=beer, amount=amount)
        return order

    @action(detail=True)
    def get_account(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        ser = AccountSerializer(order)
        return Response(ser.data)


class PaymentViewSet(ModelViewSet):
    """
        retrieve:
        Return the given Payment.

        list:
        Return a list of all the existing Payments.

        create:
        Create a new Payment.

        update:
        Update a Payment instance
    """

    queryset = Payment.objects.all().order_by("-created")
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        order = instance.order
        total_paid = sum(qs.amount for qs in order.payment_order.all())
        if (total_paid >= order.total):
            order.is_paid = True
            order.save()

        return instance

    @action(detail=False, methods=['post'])
    def equals(self, request):
        pk = self.request.data.get('order_id')
        if pk is None:
            return Response({'error': 'Missing required parameter "order_id"'}, status=status.HTTP_400_BAD_REQUEST)
        
        order = get_object_or_404(Order, id=pk)
        total = order.total
        qs = order.order_by_user.distinct('customer')
        for obj in qs:
            Payment.objects.create(order=order, customer=obj.customer,amount=total/len(qs))

        order.is_paid = True
        order.save()

        return Response("ok")

    @action(detail=False, methods=['post'])
    def by_consume(self, request):
        pk = self.request.data.get('order_id')
        if pk is None:
            return Response({'error': 'Missing required parameter "order_id"'}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, id=pk)
        dict_amount_per_user = defaultdict(int)
        for qs in order.order_by_user.all():
            dict_amount_per_user[qs.customer] += qs.amount * qs.beer.price
        
        for customer, amount in dict_amount_per_user.items():
            Payment.objects.create(order=order, customer=customer,amount=amount)

        order.is_paid = True
        order.save()

        return Response("ok")
