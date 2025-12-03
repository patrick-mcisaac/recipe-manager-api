from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from recipe.models import Ingredient
from django.contrib.auth.models import User

class IngredientTestCase(TestCase):
    def setUp(self):
        Ingredient.objects.create(name='grapes')
        Ingredient.objects.create(name='onion')

        self.user = User.objects.create_user(username='test', password='test')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.unauth_client=APIClient()

    
    def test_ingredients_exist(self):
        ingredient = Ingredient.objects.get(name='grapes')
        self.assertEqual(ingredient.name, 'grapes')

    def test_add_ingredient(self):

        response = self.client.post("/ingredients", {"name": "cheese"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.unauth_client.post('/ingredients', {'name': 'pickle'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
