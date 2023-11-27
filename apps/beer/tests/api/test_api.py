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

    def test_get_account(self):
        """
        Ensure we can get an account
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
        response = self.client.get(reverse('order-get-account', kwargs={"pk":response.data.get('id')}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('total'), 1200)
        self.assertEqual(response.data.get('is_paid'), False)


class PaymentTests(APITestCase):
    def test_pay_equal(self):
        """
        Ensure we can paid an account equally
        """

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
        response = self.client.post(reverse('order-list'), data, format='json')
        order_id = response.data.get('id')

        response = self.client.post(reverse('payment-equals'),{'order_id': order_id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.get(pk=order_id).is_paid, True)

    def test_pay_by_consume(self):
        """
        Ensure we can paid an account by consume each one
        """

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
        response = self.client.post(reverse('order-list'), data, format='json')
        order_id = response.data.get('id')

        response = self.client.post(reverse('payment-by-consume'),{'order_id': order_id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.get(pk=order_id).is_paid, True)