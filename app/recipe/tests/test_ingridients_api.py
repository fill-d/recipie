from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Ingridient
from recipe.serializers import IngridientSerializer


INGRIDIENTS_URL = reverse('recipe:ingridient-list')


class PublicIngridientApiTest(TestCase):

    def setUp(self): self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(INGRIDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngridientApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'asd@add.com',
            'test-pass'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_ingridient_list(self):
        Ingridient.objects.create(user=self.user, name='peper')
        Ingridient.objects.create(user=self.user, name='chili')

        res = self.client.get(INGRIDIENTS_URL)
        ingridients = Ingridient.objects.all().order_by('-name')
        serializer = IngridientSerializer(ingridients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingridients_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            'zxc@zxc.com',
            'test-pass'
        )
        Ingridient.objects.create(user=user2, name='peperoni')
        ingridient = Ingridient.objects.create(user=self.user, name='peper')

        res = self.client.get(INGRIDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingridient.name)

    def test_create_ingridient_success(self):
        payload = {'name': 'cabbage'}
        self.client.post(INGRIDIENTS_URL, payload)
        exists = Ingridient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_ingridient_invalid(self):
        payload = {'name': ''}
        res = self.client.post(INGRIDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
