from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from recipe.models import Recipe
from django.contrib.auth.models import User
from .ingredients import IngredientSerializer


class RecipeViewSet(ViewSet):
    def list(self, request):

        favorites = request.query_params.get("favorite", None)
        recipes = Recipe.objects.all()
        if favorites is not None and favorites == "true":
            user = request.user
            recipes = recipes.filter(favorites=user)

        serialized = RecipeSerializer(recipes, many=True, context={"request": request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            recipe = Recipe.objects.get(pk=pk)
            serialized = RecipeSerializer(
                recipe, many=False, context={"request": request}
            )
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        favorite = request.query_params.get("favorite", None)
        if favorite is not None and favorite == "true":
            try:
                recipe = Recipe.objects.get(pk=pk)
                recipe.favorites.add(request.user)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Recipe.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif favorite is not None and favorite == "false":
            try:
                recipe = Recipe.objects.get(pk=pk)
                recipe.favorites.remove(request.user)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Recipe.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)


class UserRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username"]


class RecipeSerializer(serializers.ModelSerializer):

    user = UserRecipeSerializer()
    ingredients = IngredientSerializer(many=True)
    is_favorite = serializers.SerializerMethodField()

    def get_is_favorite(self, obj):
        user = self.context["request"].user
        if obj.favorites.filter(pk=user.id).exists():
            return True
        else:
            return False

    class Meta:
        model = Recipe
        fields = [
            "id",
            "name",
            "description",
            "instructions",
            "user",
            "ingredients",
            "favorites",
            "is_favorite",
        ]
