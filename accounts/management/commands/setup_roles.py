from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create default user roles (Chef, Cook) and assign permissions"

    def handle(self, *args, **kwargs):
        chef_group, _ = Group.objects.get_or_create(name="Chef")
        cook_group, _ = Group.objects.get_or_create(name="Cook")

        # chefs have read-write access
        models = ["recipe", "step", "stepingredient", "ingredient"]
        actions = ["add", "change", "delete"]  # maybe include "view"
        wanted = [f"{a}_{m}" for m in models for a in actions]
        perms_qs = Permission.objects.filter(
            content_type__app_label="recipes",
            codename__in=wanted,
        )
        chef_group.permissions.set(perms_qs)

        # cooks have standard read-only access
        cook_group.permissions.clear()

        self.stdout.write(self.style.SUCCESS("Roles created/updated successfully"))
