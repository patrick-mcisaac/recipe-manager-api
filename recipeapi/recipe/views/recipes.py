from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from recipe.models import Recipe
from django.contrib.auth.models import User
from .ingredients import IngredientSerializer


class RecipeViewSet(ViewSet):
    def list(self, request):
        """get request for all recipes"""
        favorites = request.query_params.get("favorite", None)
        recipes = Recipe.objects.all()
        if favorites is not None and favorites == "true":
            user = request.user
            recipes = recipes.filter(favorites=user)

        serialized = RecipeSerializer(recipes, many=True, context={"request": request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """get request for single recipe"""
        try:
            recipe = Recipe.objects.get(pk=pk)
            serialized = RecipeSerializer(
                recipe, many=False, context={"request": request}
            )
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """update an existing recipe"""
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
        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = UpdateRecipeSerializer(recipe, data=request.data)
            if serializer.is_valid():
                serializer.save()
                ingredients_array = []
                for ingredient in request.data.get("ingredients"):
                    ingredients_array.append(ingredient["id"])
                recipe.ingredients.set(ingredients_array)
                serializer = RecipeSerializer(
                    recipe, many=False, context={"request": request}
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return Response(ex, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """create a new recipe"""
        try:
            user = request.user
            ingredients = request.data.get("ingredients", [])
            ingredient_list = []
            for i in ingredients:
                ingredient_list.append(i["id"])

            ingredient_list = list(set(ingredient_list))
            recipe = Recipe.objects.create(
                name=request.data.get("name"),
                description=request.data.get("description"),
                instructions=request.data.get("instructions"),
                user=user,
            )

            recipe.ingredients.set(ingredient_list)
            return Response(status=status.HTTP_201_CREATED)

        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username"]


class RecipeSerializer(serializers.ModelSerializer):

    user = UserRecipeSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True)
    is_favorite = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    def get_is_favorite(self, obj):
        user = self.context["request"].user
        if obj.favorites.filter(pk=user.id).exists():
            return True
        else:
            return False

    def get_is_owner(self, obj):
        user = self.context["request"].user
        if obj.user == user:
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
            "is_owner",
        ]


class UpdateRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            "id",
            "name",
            "description",
            "instructions",
        ]
