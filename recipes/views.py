from django.db.models import F, Min, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import (
    IngredientCreateForm,
    IngredientEditForm,
    RecipeCreateForm,
    StepCreateFormSet,
    StepIngredientCreateFormSet,
)
from .models import Ingredient, Recipe, StepIngredient


def index(request):
    return render(request, "recipes/index.html")


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


def recipe_create(request):
    if request.method == "POST":
        form = RecipeCreateForm(request.POST)
        form_steps = StepCreateFormSet(request.POST, prefix="step")
        form_stepingredients = StepIngredientCreateFormSet(prefix="stepingr")

        if form.is_valid() and form_steps.is_valid():
            recipe = form.save()

            steps = form_steps.save(commit=False)
            for i, step in enumerate(steps):
                step.recipe = recipe
                step.order_id = i
                step.save()

            return redirect("recipe_detail", recipe_slug=recipe.slug)
    else:
        form = RecipeCreateForm()
        form_steps = StepCreateFormSet(prefix="step")
        form_stepingredients = StepIngredientCreateFormSet(prefix="stepingr")

    context = {
        "form": form,
        "form_steps": form_steps,
        "form_stepingredients": form_stepingredients,
    }

    return render(request, "recipes/recipe/create.html", context)


def recipe_edit(request): ...


def ingredient_list(request):
    ingredients = Ingredient.objects.all()

    return render(request, "recipes/ingredient/list.html", {"ingredients": ingredients})


def htmx_ingredient_create(request):
    if request.method == "POST":
        form = IngredientCreateForm(request.POST)
        if form.is_valid():
            ingredient_name = form.cleaned_data["name"]
            ingr = Ingredient.objects.create(name=ingredient_name)
            context = {"ingr": ingr}
            return render(
                request, "recipes/ingredient/_create_button_oob.html", context
            )
        else:
            # return form with errors
            context = {"form": form}
            return render(request, "recipes/ingredient/_create.html", context)

    if request.method == "GET":
        if request.GET.get("action", "") == "cancel":
            return render(request, "recipes/ingredient/_create_button.html")
        else:
            form = IngredientCreateForm(initial={"name": ""})
            return render(request, "recipes/ingredient/_create.html", {"form": form})


def htmx_ingredient_edit(request, ingr_id):
    db_ingredient = get_object_or_404(Ingredient, id=ingr_id)

    if request.method == "POST":
        form = IngredientEditForm(request.POST, instance=db_ingredient)
        if form.is_valid():
            db_ingredient.name = form.cleaned_data["name"]
            db_ingredient.save()
            return render(
                request, "recipes/ingredient/_list_item.html", {"ingr": db_ingredient}
            )
        else:
            # return form with errors
            context = {"ingr": db_ingredient, "form": form}
            return render(request, "recipes/ingredient/_edit.html", context)

    if request.method == "GET":
        if request.GET.get("action", "") == "cancel":
            return render(
                request, "recipes/ingredient/_list_item.html", {"ingr": db_ingredient}
            )
        else:
            form = IngredientEditForm(instance=db_ingredient)
            context = {"ingr": db_ingredient, "form": form}
            return render(request, "recipes/ingredient/_edit.html", context)


@require_http_methods(["DELETE"])
def htmx_ingredient_delete(request, ingr_id):
    db_ingredient = get_object_or_404(Ingredient, id=ingr_id)
    db_ingredient.delete()
    return HttpResponse(status=200)
