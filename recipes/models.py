from django.db import models


class Recipe(models.Model):
    name = models.CharField(unique=True, max_length=200)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    # created_by =
    # modified_by =

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ["name"]


class Direction(models.Model): ...


class Ingredient(models.Model): ...


class Tag(models.Model): ...


class Unit(models.Model): ...


class User(models.Model): ...
