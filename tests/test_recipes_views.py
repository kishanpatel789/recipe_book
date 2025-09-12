import pytest
from django.urls import reverse


def test_index_view(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b'<h1 class="text-3xl mb-6">Recipe Book</h1>' in response.content


def test_index_view_chef(client_chef):
    response = client_chef.get("/")

    assert response.status_code == 200
    assert b'<h1 class="text-3xl mb-6">Recipe Book</h1>' in response.content
    assert b'<a href="/ingredients/">Manage Ingredients</a>' in response.content
    assert b"Logout (chef)" in response.content


def test_index_view_cook(client_cook):
    response = client_cook.get("/")

    assert response.status_code == 200
    assert b'<h1 class="text-3xl mb-6">Recipe Book</h1>' in response.content
    assert b'<a href="/ingredients/">Manage Ingredients</a>' not in response.content
    assert b"Logout (cook)" in response.content


def test_recipe_list_no_recipes(client, db):
    response = client.get("/recipes/")

    assert response.status_code == 200
    assert b"Recipes" in response.content
    assert b"<p>No recipes to show.</p>" in response.content


def test_recipe_list_with_recipes(client, db, add_recipe):
    response = client.get("/recipes/")

    assert response.status_code == 200
    assert b"Recipes" in response.content
    assert b'<a href="/recipes/test-recipe/">' in response.content
    assert b"Test Recipe" in response.content


@pytest.mark.focus
def test_recipe_detail_view(client, add_step_ingredient):
    recipe = add_step_ingredient.step.recipe
    response = client.get(reverse("recipe_detail", args=[recipe.slug]))

    assert response.status_code == 200
    assert b"Test Recipe" in response.content
    assert b"Test instruction" in response.content
    assert b"Egg" in response.content
    assert b"units" in response.content
