from django.db import models
from django.contrib.auth.models import User
from .ingredient import Ingredient


class Recipe(models.Model):

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    instructions = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    ingredients = models.ManyToManyField(Ingredient)
    favorites = models.ManyToManyField(User)
