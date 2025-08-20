from django.db.models import F, Min, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import IngredientCreateForm, IngredientEditForm
from .models import Ingredient, Recipe, StepIngredient


def index(request):
    return HttpResponse("Recipe Book is live!")


def recipe_list(request):
    recipes = Recipe.objects.all()

    return render(request, "recipes/recipe/list.html", {"recipes": recipes})


def recipe_detail(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    ingredients = (
        StepIngredient.objects.filter(step__recipe__slug=recipe_slug)
        .values(
            "ingredient__name",
            "unit__name",
            "unit__name_plural",
            "unit__abbr_singular",
            "unit__abbr_plural",
        )
        .annotate(
            quantity=Sum("quantity"),
            order_id=Min(F("step__order_id") * 100 + F("order_id")),
        )
        .order_by("order_id")
    ).all()

    return render(
        request,
        "recipes/recipe/detail.html",
        {"recipe": recipe, "ingredients": ingredients},
    )


def recipe_create(request): ...


def recipe_edit(request): ...


def ingredient_list(request):
    ingredients = Ingredient.objects.all()

    return render(request, "recipes/ingredient/list.html", {"ingredients": ingredients})


def ingredient_create(request):
    if request.method == "POST":
        form = IngredientCreateForm(request.POST)
        if form.is_valid():
            ingredient_name = form.cleaned_data["name"]

            Ingredient(name=ingredient_name).save()
            return redirect("ingredient_list")

    else:
        form = IngredientCreateForm()

    return render(request, "recipes/ingredient/create.html", {"form": form})


def ingredient_edit(request, ingr_id):
    db_ingredient = get_object_or_404(Ingredient, id=ingr_id)

    if request.method == "POST":
        form = IngredientEditForm(request.POST, instance=db_ingredient)
        if form.is_valid():
            db_ingredient = get_object_or_404(Ingredient, id=ingr_id)

            db_ingredient.name = form.cleaned_data["name"]
            db_ingredient.save()

            return redirect("ingredient_list")

    else:
        form = IngredientEditForm(instance=db_ingredient)

    return render(request, "recipes/ingredient/edit.html", {"form": form})
