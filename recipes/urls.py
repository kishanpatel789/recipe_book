from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipes/", views.recipe_list, name="recipe_list"),
    path("recipes/<str:recipe_slug>/", views.recipe_detail, name="recipe_detail"),
]
