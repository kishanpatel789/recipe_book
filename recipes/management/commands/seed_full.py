import csv
from importlib.resources import files

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Recipe, Step, StepIngredient, Tag, Unit


class Command(BaseCommand):
    help = "Seed database with sample data from CSV. WARNING: deletes existing data."

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # clear old data
        Recipe.objects.all().delete()
        Ingredient.objects.all().delete()
        Unit.objects.all().delete()
        Tag.objects.all().delete()
        Step.objects.all().delete()
        StepIngredient.objects.all().delete()

        # create tags
        tag_slugs = [
            "main-dish",
            "side-item",
            "dessert",
            "snack",
            "veggie",
            "chicken",
            "dressing",
            "bread",
            "chutney",
        ]
        Tag.objects.bulk_create([Tag(slug=slug) for slug in tag_slugs])

        # create units
        unit_content = [
            ("unit", "units", "", ""),
            ("teaspoon", "teaspoons", "tsp", "tsp"),
            ("tablespoon", "tablespoons", "tbsp", "tbsp"),
            ("ounce", "ounces", "oz", "oz"),
            ("cup", "cups", "", ""),
            ("pound", "pounds", "lb", "lbs"),
            ("bunch", "bunches", "", ""),
            ("dash", "dashes", "", ""),
            ("leaf", "leaves", "", ""),
        ]
        Unit.objects.bulk_create(
            [
                Unit(
                    name=name,
                    name_plural=name_plural,
                    abbr_singular=abbr_singular,
                    abbr_plural=abbr_plural,
                )
                for name, name_plural, abbr_singular, abbr_plural in unit_content
            ]
        )
        unit_mapper = {
            "unit": "unit",
            "tbsp": "tablespoon",
            "tsp": "teaspoon",
            "oz": "ounce",
            "c": "cup",
            "leaves": "leaf",
        }

        # parse csv file
        data_path = files("recipes.data").joinpath("seed_data.csv")
        with open(data_path, newline="\n") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["RecipeName"].strip():  # this starts a new recipe
                    recipe_name = row["RecipeName"].strip()
                    print(f"Beginning new recipe: {recipe_name}")
                    step_order_id = 0
                    recipe, _ = Recipe.objects.get_or_create(name=recipe_name)

                    if row["Tags"].strip():
                        for tag_name_raw in row["Tags"].strip().split(";"):
                            tag_name = tag_name_raw.strip().replace(" ", "")
                            tag, _ = Tag.objects.get_or_create(slug=tag_name)
                            recipe.tags.add(tag)

                    if row["ComplementaryDishes"].strip():
                        for comp_dish_raw in (
                            row["ComplementaryDishes"].strip().split(";")
                        ):
                            comp_dish_name = comp_dish_raw.strip()
                            comp, _ = Recipe.objects.get_or_create(name=comp_dish_name)
                            recipe.complementary.add(comp)

                if row["DirectionText"].strip():  # this starts a new direction
                    step_order_id += 1
                    ingredient_order_id = 0
                    instruction = row["DirectionText"].strip()
                    step = Step.objects.create(
                        recipe=recipe,
                        order_id=step_order_id,
                        instruction=instruction,
                    )
                else:  # this is an ingredient line
                    ingredient_order_id += 1
                    ingredient_quantity = row["IngredientQty"].strip()
                    ingredient_unit_raw = row["IngredientUnit"].strip()
                    ingredient_item = row["IngredientItem"].strip()
                    unit_name = unit_mapper[ingredient_unit_raw]

                    ingredient, _ = Ingredient.objects.get_or_create(
                        name=ingredient_item
                    )
                    unit = Unit.objects.get(name=unit_name)
                    StepIngredient.objects.create(
                        order_id=ingredient_order_id,
                        step=step,
                        ingredient=ingredient,
                        quantity=float(ingredient_quantity),
                        unit=unit,
                    )

        self.stdout.write(self.style.SUCCESS("Database seeded!"))
