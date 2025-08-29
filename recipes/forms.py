from django import forms
from django.forms import (
    BaseInlineFormSet,
    HiddenInput,
    inlineformset_factory,
)

from .models import Ingredient, Recipe, Step


class BaseStepFormSet(BaseInlineFormSet):
    ordering_widget = HiddenInput


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
        widgets = {"tags": forms.CheckboxSelectMultiple()}


StepCreateFormSet = inlineformset_factory(
    Recipe,
    Step,
    fields=["instruction"],
    # form=BaseStepFormSet,
    # can_order=True,
    can_delete=False,
    extra=3,
)
