from django import forms
from django.forms import (
    BaseInlineFormSet,
    HiddenInput,
    formset_factory,
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


class StepIngredientForm(forms.ModelForm):
    step_index = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = StepIngredient
        fields = ["ingredient", "quantity", "unit"]


StepCreateFormSet = inlineformset_factory(
    Recipe,
    Step,
    fields=["instruction"],
    can_delete=False,
    min_num=1,
    extra=0,
    max_num=25,
)

StepIngredientCreateFormSet = formset_factory(
    StepIngredientForm,
    can_delete=False,
    min_num=0,
    extra=0,
    max_num=50,
)
