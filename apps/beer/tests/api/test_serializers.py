from django.test import TestCase

from apps.beer.api.v1.serializers import BeerSerializer
from apps.beer.models import Beer


class BeerSerializerTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        beer = Beer.objects.create(name="IPA", price=100)
        cls.serializer = BeerSerializer(beer)

    def test_value_types(self):
        """test the types are what we expect from the serializer w full object"""

        data = self.serializer.data

        self.assertIsInstance(data["id"], int)
        self.assertIsInstance(data["name"], str)
        self.assertIsInstance(data["created"], str)
        self.assertIsInstance(data["price"], int)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        fields = {
            "id",
            "name",
            "created",
            "price",
        }
        self.assertEqual(set(data.keys()), fields)
