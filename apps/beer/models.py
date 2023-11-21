from django.db import models
from django.urls import reverse_lazy

class Beer(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    price = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"name: {self.name}"

    def get_absolute_url(self) -> reverse_lazy:
        return reverse_lazy("beer-detail", args=[str(self.id)])
