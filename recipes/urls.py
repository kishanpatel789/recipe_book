from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipes/", views.recipe_list, name="recipe_list"),
    path("recipes/<str:recipe_slug>/", views.recipe_detail, name="recipe_detail"),
    path("ingredients/", views.ingredient_list, name="ingredient_list"),
    path("ingredients/create/", views.ingredient_create, name="ingredient_create"),
    path(
        "ingredients/edit/<int:ingr_id>/", views.ingredient_edit, name="ingredient_edit"
    ),
]
