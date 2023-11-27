from django.contrib import admin

from .models import Order, OrderByUser, Payment

admin.site.register(Order)
admin.site.register(OrderByUser)
admin.site.register(Payment)
