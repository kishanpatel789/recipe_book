from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Recipe


def index(request):
    return HttpResponse("Recipe Book is live!")


def recipe_list(request):
    recipes = Recipe.objects.all()

    return render(request, "recipes/recipe/list.html", {"recipes": recipes})


def recipe_detail(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)

    return render(request, "recipes/recipe/detail.html", {"recipe": recipe})


def recipe_create(request): ...


def recipe_edit(request): ...
