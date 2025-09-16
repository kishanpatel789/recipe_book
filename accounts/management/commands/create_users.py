from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create basic chef user and cook user for demo"

    def handle(self, *args, **kwargs):
        chef_user, _ = User.objects.get_or_create(username="chef")
        chef_user.set_password("pass12345")
        chef_group = Group.objects.get(name="Chef")
        chef_user.groups.add(chef_group)

        cook_user, _ = User.objects.get_or_create(username="cook")
        cook_user.set_password("pass12345")
        cook_group = Group.objects.get(name="Cook")
        cook_user.groups.add(cook_group)

        self.stdout.write(
            self.style.SUCCESS("Users 'chef' and 'cook' created successfully")
        )
