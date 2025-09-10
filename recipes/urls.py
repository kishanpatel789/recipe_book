from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipes/", views.recipe_list, name="recipe_list"),
    path("recipes/create/", views.recipe_create, name="recipe_create"),
    path("recipes/delete/<int:pk>/", views.recipe_delete, name="recipe_delete"),
    path("recipes/<str:recipe_slug>/", views.recipe_detail, name="recipe_detail"),
    path(
        "htmx/steps/edit/<int:step_id>/",
        views.htmx_step_edit,
        name="htmx_step_edit",
    ),
    path(
        "htmx/step_ingredients/edit/<int:stepingr_id>/",
        views.htmx_step_ingredient_edit,
        name="htmx_step_ingredient_edit",
    ),
    path("ingredients/", views.ingredient_list, name="ingredient_list"),
    path(
        "htmx/ingredients/create/",
        views.htmx_ingredient_create,
        name="htmx_ingredient_create",
    ),
    path(
        "htmx/ingredients/edit/<int:ingr_id>/",
        views.htmx_ingredient_edit,
        name="htmx_ingredient_edit",
    ),
    path(
        "htmx/ingredients/delete/<int:ingr_id>/",
        views.htmx_ingredient_delete,
        name="htmx_ingredient_delete",
    ),
    path(
        "htmx/recipes/toggle_favorite/<int:recipe_id>/",
        views.htmx_toggle_favorite,
        name="htmx_toggle_favorite",
    ),
]
