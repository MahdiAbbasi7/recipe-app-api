"""
Serializers for recipe apis.
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
    Ingredient,
    )


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class RecipeSerializers(serializers.ModelSerializer):
    """Serializer for recipe"""
    tags = TagSerializer(many=True, required=True)
    ingerdiants = IngredientSerializer(many=True,required=False)


    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'time_minutes', 'price', 'link', 'tags',
            'ingerdiants',
            ]
        read_only_fields = ['id']
    
    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_ingrediant(self, ingerdiants, recipe):
        """Handle getting or creating an ingrediant as needed."""
        auth_user = self.context['request'].user
        for ingrediant in ingerdiants:
            ingrediant.obj, create = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingrediant,
            )
            recipe.ingerdiants.add(ingrediant)
    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop('tags', [])
        ingerdiants  = validated_data.pop('ingerdiants', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingrediant(ingerdiants, recipe)

        return recipe
    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags', None)
        ingrediant = validated_data.pop('ingrediant', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        
        if ingrediant is not None:
            instance.ingrediant.clear()
            self._get_or_create_ingredients(ingrediant, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class RecipeDetailSerializer(RecipeSerializers):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializers.Meta):
        fields = RecipeSerializers.Meta.fields + ['description']