from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create default user roles (Chef, Cook) and assign permissions"

    def handle(self, *args, **kwargs):
        chef_group, _ = Group.objects.get_or_create(name="Chef")
        cook_group, _ = Group.objects.get_or_create(name="Cook")

        # chefs have read-write access
        chef_permissions = []
        for model in ["recipe", "step", "stepingredient", "ingredient"]:
            for action in ["add", "change", "delete"]:
                chef_permissions.append(
                    Permission.objects.get(
                        codename=f"{action}_{model}", content_type__app_label="recipes"
                    )
                )
        chef_group.permissions.set(chef_permissions)
        chef_group.save()

        # cooks have standard read-only access
        cook_group.permissions.clear()

        self.stdout.write(self.style.SUCCESS("Roles created/updated successfully"))
