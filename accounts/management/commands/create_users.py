from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create basic chef user and cook user for demo"

    def handle(self, *args, **kwargs):
        chef_user = User.objects.create_user(username="chef", password="pass12345")
        chef_group = Group.objects.get(name="Chef")
        chef_user.groups.add(chef_group)

        cook_user = User.objects.create_user(username="cook", password="pass12345")
        cook_group = Group.objects.get(name="Cook")
        cook_user.groups.add(cook_group)

        self.stdout.write(self.style.SUCCESS("Chef and cook user created successfully"))
