from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    group_names = ['student', 'instructor', 'organiser']
    def handle(self, *args, **kwargs):
        for group_name in self.group_names:
            group, status = Group.objects.get_or_create(name=group_name)
            if status:
                self.stdout.write("Group {} created.".format(group_name))
            else:
                self.stdout.write("Group {} already exists.".format(group_name))
        self.stdout.write("Successfully populated groups")