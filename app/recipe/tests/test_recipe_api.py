from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Recipe, Tag, Ingridient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_recipe(user, **params):
    defaults = {
        'title': 'sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


def sample_tag(user, name='main course'):
    return Tag.objects.create(user=user, name=name)


def sample_ingridient(user, name='main ingridient'):
    return Ingridient.objects.create(user=user, name=name)


class PublicRecipeApiTest(TestCase):

    def setUp(self): self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'asd@add.com',
            'test-pass'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_recipes(self):
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            'zxc@zxc.com',
            'test-pass'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingridients.add(sample_ingridient(user=self.user))
        url = detail_url(recipe.id)

        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)

    def test_creat_basic_recipe(self):
        payload = {
            'title': 'chocolate cheesecake',
            'time_minutes': 30,
            'price': 5.00
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_creat_recipe_with_tags(self):
        tag1 = sample_tag(user=self.user, name='chocolate')
        tag2 = sample_tag(user=self.user, name='cheese')
        payload = {
            'title': 'chocolate cheesecake',
            'time_minutes': 30,
            'price': 5.00,
            'tags': [tag1.id, tag2.id]
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_creat_recipe_with_ingridients(self):
        ingridient1 = sample_ingridient(user=self.user, name='chocolate')
        ingridient2 = sample_ingridient(user=self.user, name='cheese')
        payload = {
            'title': 'chocolate cheesecake',
            'time_minutes': 30,
            'price': 5.00,
            'ingridients': [ingridient1.id, ingridient2.id]
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        ingridients = recipe.ingridients.all()
        self.assertEqual(ingridients.count(), 2)
        self.assertIn(ingridient1, ingridients)
        self.assertIn(ingridient2, ingridients)
