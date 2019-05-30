from django.core.management.base import BaseCommand
from api.models import ActivityCategories

class Command(BaseCommand):
    category_names = ['swimming', 'hiking', 'cricket', 'music', 'tennis']

    def handle(self, *args, **kwargs):
        for category_name in self.category_names:
            category, status = ActivityCategories.get_or_create(category_name)
            if status:
                self.stdout.write("Category {} created.".format(category_name))
            else:
                self.stdout.write("Category {} already exists.".format(category_name))
        self.stdout.write("Successfully populated categories.")
