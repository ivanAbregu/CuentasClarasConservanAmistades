from django.test import TestCase
from apps.beer.models import Beer


class BeerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.beer = Beer.objects.create(name="IPA", price=100)

    def test_name_label(self):
        field_label = self.beer._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_price_label(self):
        field_label = self.beer._meta.get_field("price").verbose_name
        self.assertEquals(field_label, "price")

    def test_get_absolute_url(self):
        # This will also fail if the urlconf is not defined.
        self.assertEquals(self.beer.get_absolute_url(), f"/api/v1/beer/{self.beer.id}/")

    def test_object_to_str(self):
        expected_object_name = f"name: {self.beer.name}"
        self.assertEquals(expected_object_name, str(self.beer))

    # --TEST DEFAULTS VALUES

    def test_created_default(self):
        self.assertTrue(self.beer.created)