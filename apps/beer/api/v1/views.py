from rest_framework.viewsets import ModelViewSet

from apps.beer.models import Beer
from .serializers import BeerSerializer


class BeerViewSet(ModelViewSet):
    """
        retrieve:
        Return the given Beer.

        list:
        Return a list of all the existing Beers.

        create:
        Create a new Beer instance.

        update:
        Update a Beer instance
    """

    queryset = Beer.objects.all().order_by("-created")
    serializer_class = BeerSerializer
    http_method_names = ["get", "post", "put", "patch"]
