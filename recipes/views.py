from django.http import HttpResponse
from django.shortcuts import render

from .models import Recipe


def index(request):
    return HttpResponse("Recipe Book is live!")


def recipe_list(request):
    recipes = Recipe.objects.all()

    return render(request, "recipes/recipe/list.html", {"recipes": recipes})


def recipe_detail(request): ...


def recipe_create(request): ...


def recipe_edit(request): ...
