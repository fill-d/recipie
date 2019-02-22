from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='asd@asd.com', password='test-pass'):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_succesfull(self):
        e = 'asd@asd.com'
        p = 'test-pass'
        u = get_user_model().objects.create_user(
            email=e,
            password=p
        )

        self.assertEqual(u.email, e)
        self.assertTrue(u.check_password(p))

    def test_new_user_email_normalized(self):
        e = 'asd@ASD.COM'
        u = get_user_model().objects.create_user(e, 'test-pass')

        self.assertEqual(u.email, e.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test-pass')

    def test_creating_new_superuser(self):
        su = get_user_model().objects.create_superuser('asd@asd.com',
                                                       'test-pass')
        self.assertTrue(su.is_superuser)
        self.assertTrue(su.is_staff)

    def test_tag_str_repr(self):
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingridient_string(self):
        ingridient = models.Ingridient.objects.create(
            user=sample_user(),
            name='cucumber'
        )

        self.assertEqual(str(ingridient), ingridient.name)

    def test_recipe_str(self):
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='steak and mashroom ssuce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)
