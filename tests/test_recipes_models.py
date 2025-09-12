import pytest

from recipes.models import Ingredient, Recipe, Tag, Unit


@pytest.fixture
def add_tags(db):
    tag_main = Tag.objects.create(slug="main-dish")
    tag_side = Tag.objects.create(slug="side-item")

    return {"tag_main": tag_main, "tag_side": tag_side}


@pytest.fixture
def add_units(db):
    unit_unit = Unit.objects.create(name="unit", name_plural="units")
    unit_teaspoon = Unit.objects.create(
        name="teaspoon",
        name_plural="teaspoons",
        abbr_singular="tsp",
        abbr_plural="tsp",
    )

    return {"unit_unit": unit_unit, "unit_teaspoon": unit_teaspoon}


@pytest.fixture
def add_ingredients(db):
    ingr_egg = Ingredient.objects.create(name="Egg")
    ingr_flour = Ingredient.objects.create(name="All Purpose Flour")

    return {"ingr_egg": ingr_egg, "ingr_flour": ingr_flour}


@pytest.fixture
def add_recipe(db, add_tags):
    recipe = Recipe.objects.create(
        name="Test Recipe",
    )
    recipe.tags.add(add_tags["tag_main"])

    return recipe


@pytest.fixture
def add_step(add_recipe):
    step = add_recipe.steps.create(order_id=1, instruction="Test instruction")
    return step


def test_create_recipe(add_recipe):
    recipe = add_recipe
    assert recipe.id is not None
    assert recipe.name == "Test Recipe"
    assert recipe.slug == "test-recipe"
    assert recipe.created_at is not None
    assert recipe.modified_at is not None
    assert str(recipe) == recipe.name


def test_create_step(add_step):
    step = add_step
    assert step.id is not None
    assert step.order_id == 1
    assert step.instruction == "Test instruction"
    assert str(step) == f"{step.recipe.slug}/{step.order_id}"


def test_create_step_ingredient(add_step, add_units, add_ingredients):
    step = add_step
    ingredient = add_ingredients["ingr_egg"]
    unit = add_units["unit_unit"]
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
        == f"{step.recipe.slug}/{step.order_id}/{step_ingredient.order_id}"
    )


def test_create_ingredient(add_ingredients):
    ingredient = add_ingredients["ingr_egg"]
    assert ingredient.id is not None
    assert ingredient.name == "Egg"
    assert str(ingredient) == ingredient.name


def test_create_tag(add_tags):
    tag = add_tags["tag_main"]
    assert tag.id is not None
    assert tag.slug == "main-dish"
    assert str(tag) == tag.slug


def test_tag_uniqueness(add_tags):
    dup_tag = Tag.objects.create(slug="main-dish")
    assert dup_tag.slug == "main-dish-1"


def test_create_unit(add_units):
    unit = add_units["unit_teaspoon"]
    assert unit.id is not None
    assert unit.name == "teaspoon"
    assert unit.name_plural == "teaspoons"
    assert unit.abbr_singular == "tsp"
    assert unit.abbr_plural == "tsp"
    assert str(unit) == unit.name
