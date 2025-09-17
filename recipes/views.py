from django.contrib.auth.decorators import permission_required
from django.db.models import F, Min, Prefetch, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import (
    IngredientCreateForm,
    IngredientEditForm,
    RecipeCreateForm,
    StepCreateFormSet,
    StepEditForm,
    StepIngredientCreateFormSet,
    StepIngredientEditForm,
)
from .helpers import determine_is_chef, get_favorite_recipes, update_recipe_modified
from .models import Ingredient, Recipe, Step, StepIngredient


def index(request):
    is_chef = determine_is_chef(request.user)
    context = {"is_chef": is_chef}

    return render(request, "recipes/index.html", context)


def recipe_list(request):
    recipes = Recipe.objects.all()
    favorites = get_favorite_recipes(request.user)
    is_chef = determine_is_chef(request.user)
    context = {
        "recipes": recipes,
        "favorites": favorites,
        "is_chef": is_chef,
    }

    return render(request, "recipes/recipe/list.html", context)


def recipe_detail(request, recipe_slug):
    recipe_qs = (
        Recipe.objects.prefetch_related("tags")
        .prefetch_related("complementary")
        .prefetch_related(
            Prefetch(
                "steps",
                queryset=Step.objects.prefetch_related(
                    Prefetch(
                        "ingredients",
                        queryset=StepIngredient.objects.select_related(
                            "ingredient", "unit"
                        ),
                    )
                ),
            )
        )
        .filter(slug=recipe_slug)
        .only("id", "name", "slug")
    )
    recipe = get_object_or_404(recipe_qs)

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

    is_chef = determine_is_chef(request.user)
    if is_chef:
        edit_mode = request.GET.get("action", "") == "edit"
    else:
        edit_mode = False

    if request.user.is_authenticated:
        is_fav = recipe in request.user.profile.favorites.all()
    else:
        is_fav = False

    context = {
        "recipe": recipe,
        "ingredients": ingredients,
        "edit_mode": edit_mode,
        "is_chef": is_chef,
        "is_fav": is_fav,
    }

    return render(
        request,
        "recipes/recipe/detail.html",
        context,
    )


@permission_required("recipes.add_recipe")
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
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.modified_by = request.user
            recipe.save()
            form.save_m2m()

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


@require_POST
@permission_required("recipes.delete_recipe")
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.POST:
        recipe.delete()
        return redirect("recipe_list")


@permission_required("recipes.change_step")
def htmx_step_edit(request, step_id):
    db_step = get_object_or_404(Step, id=step_id)

    if request.method == "POST":
        form = StepEditForm(request.POST, instance=db_step)
        if form.is_valid():
            db_step = form.save()
            update_recipe_modified(db_step.recipe, request.user)
            context = {
                "step": db_step,
                "edit_mode": True,
            }
            return render(request, "recipes/step/_list_item.html", context)
        else:
            # return form with errors
            context = {"step": db_step, "form": form}
            return render(request, "recipes/step/_edit.html", context)

    if request.method == "GET":
        if request.GET.get("action", "") == "cancel":
            context = {
                "step": db_step,
                "edit_mode": True,
            }
            return render(request, "recipes/step/_list_item.html", context)
        else:
            form = StepEditForm(instance=db_step)
            context = {"step": db_step, "form": form}
            return render(request, "recipes/step/_edit.html", context)


@permission_required("recipes.change_stepingredient")
def htmx_step_ingredient_edit(request, stepingr_id):
    db_stepingr = get_object_or_404(StepIngredient, id=stepingr_id)

    if request.method == "POST":
        form = StepIngredientEditForm(request.POST, instance=db_stepingr)
        if form.is_valid():
            db_stepingr = form.save()
            update_recipe_modified(db_stepingr.step.recipe, request.user)
            context = {
                "stepingr": db_stepingr,
                "edit_mode": True,
            }
            return render(request, "recipes/step_ingredient/_list_item.html", context)
        else:
            # return form with errors
            context = {"stepingr": db_stepingr, "form": form}
            return render(request, "recipes/step_ingredient/_edit.html", context)

    if request.method == "GET":
        if request.GET.get("action", "") == "cancel":
            context = {
                "stepingr": db_stepingr,
                "edit_mode": True,
            }
            return render(request, "recipes/step_ingredient/_list_item.html", context)
        else:
            form = StepIngredientEditForm(instance=db_stepingr)
            context = {"stepingr": db_stepingr, "form": form}
            return render(request, "recipes/step_ingredient/_edit.html", context)


@permission_required("recipes.change_ingredient")
def ingredient_list(request):
    ingredients = Ingredient.objects.all()

    return render(request, "recipes/ingredient/list.html", {"ingredients": ingredients})


@permission_required("recipes.add_ingredient")
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


@permission_required("recipes.change_ingredient")
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
@permission_required("recipes.delete_ingredient")
def htmx_ingredient_delete(request, ingr_id):
    db_ingredient = get_object_or_404(Ingredient, id=ingr_id)
    db_ingredient.delete()
    return HttpResponse(status=200)


@require_POST
def htmx_toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    profile = request.user.profile

    if recipe in profile.favorites.all():
        profile.favorites.remove(recipe)
        return render(request, "recipes/icons/not_favorite.html")
    else:
        profile.favorites.add(recipe)
        return render(request, "recipes/icons/favorite.html")
