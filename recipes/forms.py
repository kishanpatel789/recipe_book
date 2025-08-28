from django import forms

from .models import Ingredient, Recipe


class IngredientCreateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name"]


class IngredientEditForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name"]


class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "tags", "complementary"]
