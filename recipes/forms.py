from django import forms
from django.forms import (
    BaseInlineFormSet,
    HiddenInput,
    inlineformset_factory,
)

from .models import Ingredient, Recipe, Step, StepIngredient


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
    min_num=1,
    extra=0,
    max_num=25,
)

StepIngredientCreateFormSet = inlineformset_factory(
    Step,
    StepIngredient,
    fields=["ingredient", "quantity", "unit"],
    can_delete=False,
    min_num=0,
    extra=3,
    max_num=10,
)
