from rest_framework import serializers

# from apps.cell.api.v1.serializers import CellSerializer
from apps.beer.models import Beer


class BeerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Beer

        fields = (
            "id",
            "name",
            "created",
            "price",
        )
