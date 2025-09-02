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
        form_stepingredients = StepIngredientCreateFormSet(
            request.POST, prefix="stepingr"
        )

        if all(
            [form.is_valid(), form_steps.is_valid(), form_stepingredients.is_valid()]
        ):
            recipe = form.save()

            steps = form_steps.save(commit=False)
            step_map = {}
            for i, step in enumerate(steps):
                step.recipe = recipe
                step.order_id = i
                step.save()
                step_map[i] = step

            step_index = 0
            stepingr_order_id = 0
            for ingr_form in form_stepingredients.cleaned_data:
                if not ingr_form or ingr_form.get("ingredient") is None:
                    continue

                form_step_index = int(ingr_form["step_index"])
                if form_step_index != step_index:
                    step_index = form_step_index
                    stepingr_order_id = 0

                step_instance = step_map.get(form_step_index)

                StepIngredient.objects.create(
                    step=step_instance,
                    ingredient=ingr_form["ingredient"],
                    order_id=stepingr_order_id,
                    quantity=ingr_form["quantity"],
                    unit=ingr_form["unit"],
                )

                stepingr_order_id += 1

            return redirect("recipe_detail", recipe_slug=recipe.slug)
    else:
        form = RecipeCreateForm()
        form_steps = StepCreateFormSet(prefix="step")
        form_stepingredients = StepIngredientCreateFormSet(prefix="stepingr")

    grouped_ingredients = {}
    for ingr_form in form_stepingredients:
        step_index = ingr_form["step_index"].value()
        grouped_ingredients.setdefault(step_index, []).append(ingr_form)

    context = {
        "form": form,
        "form_steps": form_steps,
        "form_stepingredients": form_stepingredients,
        "grouped_ingredients": grouped_ingredients,
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
