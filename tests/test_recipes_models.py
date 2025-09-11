import pytest

from recipes.models import Recipe


@pytest.mark.django_db
def test_create_recipe():
    recipe = Recipe.objects.create(
        name="Test Recipe",
    )
    assert recipe.id is not None
    assert recipe.name == "Test Recipe"
    assert recipe.slug == "test-recipe"
