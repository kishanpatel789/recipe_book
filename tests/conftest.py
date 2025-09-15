import itertools

import pytest
from django.contrib.auth.models import Group, Permission

from recipes.models import Ingredient, Recipe, Tag, Unit


@pytest.fixture
def client_chef(client, db, django_user_model):
    user = django_user_model.objects.create_user(username="chef", password="pass12345")
    chef_group, _ = Group.objects.get_or_create(name="Chef")
    models = ["recipe", "step", "stepingredient", "ingredient"]
    actions = ["add", "change", "delete"]
    chef_permissions = set()
    for model, action in itertools.product(models, actions):
        chef_permissions.add(
            Permission.objects.get(
                codename=f"{action}_{model}", content_type__app_label="recipes"
            )
        )
    chef_group.permissions.set(chef_permissions)
    chef_group.save()
    user.groups.add(chef_group)

    client.force_login(user)

    return client


@pytest.fixture
def client_cook(client, db, django_user_model):
    user = django_user_model.objects.create_user(username="cook", password="pass12345")
    cook_group, _ = Group.objects.get_or_create(name="Cook")
    cook_group.permissions.clear()
    cook_group.save()
    user.groups.add(cook_group)

    client.force_login(user)

    return client


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


@pytest.fixture
def add_step_ingredient(add_step, add_units, add_ingredients):
    ingredient = add_ingredients["ingr_egg"]
    unit = add_units["unit_unit"]
    step_ingredient = add_step.ingredients.create(
        order_id=1, ingredient=ingredient, quantity=2, unit=unit
    )
    return step_ingredient
