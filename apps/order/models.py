from django.db import models
from django.urls import reverse_lazy
from apps.beer.models import Beer
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    
    @property
    def total(self) -> int:
        return sum(qs.beer.price * qs.amount for qs in self.order_by_user.all())

    def __str__(self) -> str:
        return f"id: {self.id}"

class OrderByUser(models.Model):
    order = models.ForeignKey(Order, related_name="order_by_user", on_delete=models.CASCADE)
    customer = models.ForeignKey(User, related_name="order_customer", on_delete=models.CASCADE)
    beer = models.ForeignKey(Beer, related_name="beer_order_by_user", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f"user {self.customer.username} ordered {self.amount} {self.beer.name} beers"


class Payment(models.Model):
    order = models.ForeignKey(Order, related_name="payment_order", on_delete=models.CASCADE)
    customer = models.ForeignKey(User, related_name="payment_customer", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f"user {self.customer.username} paid {self.amount}"

