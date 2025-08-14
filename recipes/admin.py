from django.contrib import admin

from recipes.models import Ingredient, Recipe, Step, StepIngredient, Tag, Unit


class StepIngredientInline(admin.TabularInline):
    model = StepIngredient
    extra = 1
    autocomplete_fields = ("ingredient", "unit")
    ordering = ("order_id",)


class StepInline(admin.TabularInline):
    model = Step
    extra = 1
    ordering = ("order_id",)
    show_change_link = True
    inlines = [StepIngredientInline]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at", "modified_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ["name"]}
    filter_horizontal = ("tags", "complementary")
    date_hierarchy = "created_at"
    ordering = ("name",)
    inlines = [StepInline]


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ("recipe", "order_id", "instruction")
    search_fields = ("instruction", "recipe__name")
    list_filter = ("recipe",)
    ordering = ("recipe", "order_id")
    inlines = [StepIngredientInline]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("name", "name_plural", "abbr_singular", "abbr_plural")
    search_fields = ("name", "name_plural", "abbr_singular", "abbr_plural")
    ordering = ("name",)


@admin.register(StepIngredient)
class StepIngredientAdmin(admin.ModelAdmin):
    list_display = ("step", "ingredient", "order_id", "quantity", "unit")
    search_fields = ("step__recipe__name", "ingredient__name")
    list_filter = ("unit",)
    ordering = ("step", "order_id")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("slug",)
    search_fields = ("slug",)
    ordering = ("slug",)
