from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from recipe.models import Ingredient


class IngredientViewSet(ViewSet):
    def list(self, request):
        ingredients = Ingredient.objects.all()
        serialized = IngredientSerializer(ingredients, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ["id", "name"]
