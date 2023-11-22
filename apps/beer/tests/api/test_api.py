from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.order.models import Order, OrderByUser
from apps.beer.models import Beer
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderTests(APITestCase):
    def test_create_order_one_user(self):
        """
        Ensure we can create a new Order object.
        """
        url = reverse('order-list')
        beer_name = 'red'
        username = 'user1'
        data = {username:{beer_name:1}}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderByUser.objects.count(), 1)
        self.assertEqual(Beer.objects.count(), 1)
        self.assertEqual(Beer.objects.get().name, beer_name)
        self.assertEqual(User.objects.get().username, username)

    def test_create_order_three_users(self):
        """
        Ensure we can create a new Order object.
        """
        url = reverse('order-list')
        red = 'red'
        ipa = 'ipa'
        blonde = 'blonde'
        user1 = 'Ivan'
        user2 = 'Pedro'
        user3 = 'Gaspar'
        data = {
            user1:{red:2, ipa:3},
            user2:{blonde:1},
            user3:{red:1, ipa:2, blonde:3},
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderByUser.objects.count(), 6)
        self.assertEqual(Beer.objects.count(), 3)
        self.assertEqual(Beer.objects.first().name, red)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.first().username, user1)

    def test_create_2_orders(self):
        """
        Ensure we can create a new Order object.
        """
        url = reverse('order-list')
        red = 'red'
        ipa = 'ipa'
        blonde = 'blonde'
        user1 = 'Ivan'
        user2 = 'Pedro'
        user3 = 'Gaspar'
        data = {
            user1:{red:2, ipa:3},
            user2:{blonde:1},
            user3:{red:1, ipa:2, blonde:3},
        }
        response = self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(OrderByUser.objects.count(), 12)
        self.assertEqual(Beer.objects.count(), 3)
        self.assertEqual(Beer.objects.first().name, red)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.first().username, user1)
