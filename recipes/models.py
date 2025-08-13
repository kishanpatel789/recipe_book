from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    slug = models.SlugField(unique=True, max_length=50)

    def save(self, *args, **kwargs):
        base_slug = slugify(self.slug)
        slug = base_slug
        counter = 1

        # Ensure uniqueness of the slug
        while Tag.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ["slug"]


class Recipe(models.Model):
    name = models.CharField(unique=True, max_length=200)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    # created_by =
    # modified_by =
    tags = models.ManyToManyField(Tag)
    complementary = models.ManyToManyField("self", symmetrical=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            # Ensure uniqueness of the slug
            while Recipe.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Step(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="steps", on_delete=models.CASCADE)
    order_id = models.SmallIntegerField()
    instruction = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.recipe.name} {self.order_id}"

    class Meta:
        ordering = ["order_id"]


class Unit(models.Model):
    name = models.CharField(unique=True, max_length=20)
    name_plural = models.CharField(unique=True, max_length=20)
    abbr_singular = models.CharField(max_length=10)
    abbr_plural = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Ingredient(models.Model):
    step = models.ForeignKey(Step, related_name="ingredients", on_delete=models.CASCADE)
    order_id = models.SmallIntegerField()
    quantity = models.FloatField(null=True)
    unit = models.ForeignKey(Unit, null=True, on_delete=models.SET_NULL)
    item = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.item}"

    class Meta:
        ordering = ["order_id"]
