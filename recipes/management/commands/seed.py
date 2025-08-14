from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Recipe, Step, StepIngredient, Tag, Unit


class Command(BaseCommand):
    help = "Seed database with sample data. WARNING: deletes existing data."

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
        Tag.objects.create(slug="main-dish")
        tag_side = Tag.objects.create(slug="side-item")
        tag_dessert = Tag.objects.create(slug="dessert")
        Tag.objects.create(slug="snack")
        Tag.objects.create(slug="veggie")
        Tag.objects.create(slug="chicken")
        Tag.objects.create(slug="dressing")
        Tag.objects.create(slug="bread")
        Tag.objects.create(slug="chutney")

        # create units
        unit_unit = Unit.objects.create(name="unit", name_plural="units")
        unit_teaspoon = Unit.objects.create(
            name="teaspoon",
            name_plural="teaspoons",
            abbr_singular="tsp",
            abbr_plural="tsp",
        )
        Unit.objects.create(
            name="tablespoon",
            name_plural="tablespoons",
            abbr_singular="tbsp",
            abbr_plural="tbsp",
        )
        Unit.objects.create(
            name="ounce", name_plural="ounces", abbr_singular="oz", abbr_plural="oz"
        )
        unit_cup = Unit.objects.create(name="cup", name_plural="cups")
        Unit.objects.create(
            name="pound", name_plural="pounds", abbr_singular="lb", abbr_plural="lbs"
        )
        Unit.objects.create(name="bunch", name_plural="bunches")
        Unit.objects.create(name="dash", name_plural="dashes")
        Unit.objects.create(name="leaf", name_plural="leaves")

        # create ingredients
        ingr_brownsugar = Ingredient.objects.create(name="Brown Sugar")
        ingr_butterroom = Ingredient.objects.create(name="Butter (room temperature)")
        ingr_egg = Ingredient.objects.create(name="Egg")
        ingr_vanilla = Ingredient.objects.create(name="Vanilla")
        ingr_flour = Ingredient.objects.create(name="All Purpose Flour")
        ingr_bakingsoda = Ingredient.objects.create(name="Baking Soda")
        ingr_salt = Ingredient.objects.create(name="Salt")
        ingr_chocchips = Ingredient.objects.create(name="Semi-Sweet Chocolate Chips")
        ingr_yogurt = Ingredient.objects.create(name="Yogurt")
        ingr_greenchili = Ingredient.objects.create(name="Green Chili")
        ingr_water = Ingredient.objects.create(name="Water")
        ingr_cumin = Ingredient.objects.create(name="Cumin")
        ingr_garlic = Ingredient.objects.create(name="Garlic")
        ingr_cilantrochop = Ingredient.objects.create(name="Cilantro (chopped)")

        # create recipe 1
        rec_cookies = Recipe.objects.create(name="Chocolate Chip Cookies")
        rec_cookies.tags.add(tag_dessert)

        Step.objects.create(
            recipe=rec_cookies, order_id=1, instruction="Preheat to 365 degrees."
        )

        step2 = Step.objects.create(
            recipe=rec_cookies, order_id=2, instruction="Combine:"
        )
        StepIngredient.objects.create(
            order_id=1,
            step=step2,
            ingredient=ingr_brownsugar,
            quantity=1.25,
            unit=unit_cup,
        )
        StepIngredient.objects.create(
            order_id=2,
            step=step2,
            ingredient=ingr_butterroom,
            quantity=0.5,
            unit=unit_cup,
        )
        StepIngredient.objects.create(
            order_id=3, step=step2, ingredient=ingr_egg, quantity=2, unit=unit_unit
        )
        StepIngredient.objects.create(
            order_id=4,
            step=step2,
            ingredient=ingr_vanilla,
            quantity=1,
            unit=unit_teaspoon,
        )

        step3 = Step.objects.create(
            recipe=rec_cookies, order_id=3, instruction="Combine:"
        )
        StepIngredient.objects.create(
            order_id=1, step=step3, ingredient=ingr_flour, quantity=2.5, unit=unit_cup
        )
        StepIngredient.objects.create(
            order_id=2,
            step=step3,
            ingredient=ingr_bakingsoda,
            quantity=1.5,
            unit=unit_teaspoon,
        )
        StepIngredient.objects.create(
            order_id=3,
            step=step3,
            ingredient=ingr_salt,
            quantity=0.5,
            unit=unit_teaspoon,
        )

        Step.objects.create(
            recipe=rec_cookies, order_id=4, instruction="Combine wet and dry mixtures."
        )

        step5 = Step.objects.create(recipe=rec_cookies, order_id=5, instruction="Add:")
        StepIngredient.objects.create(
            order_id=1,
            step=step5,
            ingredient=ingr_chocchips,
            quantity=1.25,
            unit=unit_cup,
        )

        Step.objects.create(
            recipe=rec_cookies,
            order_id=6,
            instruction="Chill dough in fridge for at least 2 hours.",
        )

        Step.objects.create(
            recipe=rec_cookies, order_id=7, instruction="Roll dough into 1 inch balls."
        )

        Step.objects.create(
            recipe=rec_cookies,
            order_id=8,
            instruction="Bake for 10-12 minutes or until golden brown.",
        )

        # create recipe 2
        rec_chaas = Recipe.objects.create(name="Chaas")
        rec_chaas.tags.add(tag_side)

        rec_cookies.complementary.add(rec_chaas)

        step1 = Step.objects.create(recipe=rec_chaas, order_id=1, instruction="Blend:")
        StepIngredient.objects.create(
            order_id=1, step=step1, ingredient=ingr_yogurt, quantity=1.5, unit=unit_cup
        )
        StepIngredient.objects.create(
            order_id=2,
            step=step1,
            ingredient=ingr_greenchili,
            quantity=0.5,
            unit=unit_teaspoon,
        )
        StepIngredient.objects.create(
            order_id=3,
            step=step1,
            ingredient=ingr_salt,
            quantity=0.75,
            unit=unit_teaspoon,
        )
        StepIngredient.objects.create(
            order_id=4, step=step1, ingredient=ingr_water, quantity=1, unit=unit_cup
        )
        StepIngredient.objects.create(
            order_id=5, step=step1, ingredient=ingr_water, quantity=1, unit=unit_cup
        )
        StepIngredient.objects.create(
            order_id=6,
            step=step1,
            ingredient=ingr_cumin,
            quantity=0.5,
            unit=unit_teaspoon,
        )
        StepIngredient.objects.create(
            order_id=7,
            step=step1,
            ingredient=ingr_garlic,
            quantity=0.25,
            unit=unit_teaspoon,
        )
        StepIngredient.objects.create(
            order_id=8,
            step=step1,
            ingredient=ingr_cilantrochop,
            quantity=2,
            unit=unit_teaspoon,
        )

        Step.objects.create(
            recipe=rec_chaas, order_id=2, instruction="Store in fridge."
        )

        self.stdout.write(self.style.SUCCESS("Database seeded!"))
