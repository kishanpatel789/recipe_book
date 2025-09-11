import pytest

from recipes.models import Ingredient, Recipe, Tag, Unit


@pytest.fixture
def add_tags(db):
    Tag.objects.create(slug="main-dish")
    Tag.objects.create(slug="side-item")


@pytest.fixture
def add_units(db):
    Unit.objects.create(name="unit", name_plural="units")
    Unit.objects.create(
        name="teaspoon",
        name_plural="teaspoons",
        abbr_singular="tsp",
        abbr_plural="tsp",
    )


@pytest.fixture
def add_ingredients(db):
    Ingredient.objects.create(name="Egg")
    Ingredient.objects.create(name="All Purpose Flour")


@pytest.fixture
def add_recipe(db, add_tags):
    recipe = Recipe.objects.create(
        name="Test Recipe",
    )

    recipe.tags.add(Tag.objects.get(slug="main-dish"))

    return recipe


def test_create_recipe(add_recipe):
    assert add_recipe.id is not None
    assert add_recipe.name == "Test Recipe"
    assert add_recipe.slug == "test-recipe"
    assert add_recipe.created_at is not None
    assert add_recipe.modified_at is not None
    assert str(add_recipe) == add_recipe.name


def test_create_step(add_recipe):
    step = add_recipe.steps.create(order_id=1, instruction="Test instruction")
    assert step.id is not None
    assert step.order_id == 1
    assert step.instruction == "Test instruction"
    assert str(step) == f"{add_recipe.slug}/{step.order_id}"


def test_create_step_ingredient(add_recipe, add_units, add_ingredients):
    step = add_recipe.steps.create(order_id=1, instruction="Test instruction")
    ingredient = Ingredient.objects.get(name="Egg")
    unit = Unit.objects.get(name="unit")
    step_ingredient = step.ingredients.create(
        order_id=1, ingredient=ingredient, quantity=2, unit=unit
    )
    assert step_ingredient.id is not None
    assert step_ingredient.order_id == 1
    assert step_ingredient.ingredient == ingredient
    assert step_ingredient.quantity == 2
    assert step_ingredient.unit == unit
    assert (
        str(step_ingredient)
        == f"{add_recipe.slug}/{step.order_id}/{step_ingredient.order_id}"
    )


def test_create_ingredient(add_ingredients):
    ingredient = Ingredient.objects.get(name="Egg")
    assert ingredient.id is not None
    assert ingredient.name == "Egg"
    assert str(ingredient) == ingredient.name


def test_create_tag(add_tags):
    tag = Tag.objects.get(slug="main-dish")
    assert tag.id is not None
    assert tag.slug == "main-dish"
    assert str(tag) == tag.slug


def test_tag_uniqueness(add_tags):
    dup_tag = Tag.objects.create(slug="main-dish")
    assert dup_tag.slug == "main-dish-1"


def test_create_unit(add_units):
    unit = Unit.objects.get(name="teaspoon")
    assert unit.id is not None
    assert unit.name == "teaspoon"
    assert unit.name_plural == "teaspoons"
    assert unit.abbr_singular == "tsp"
    assert unit.abbr_plural == "tsp"
    assert str(unit) == unit.name
