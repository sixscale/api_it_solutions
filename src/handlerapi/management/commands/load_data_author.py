import json
import os

from django.core.management.base import BaseCommand

from handlerapi.models import AuthorAdvertisement

from config.settings import BASE_DIR

data_file_path = os.path.join(BASE_DIR, 'fixtures/data_author.json')


class Command(BaseCommand):
    help = 'Load data from JSON file into the database'

    def handle(self, *args, **kwargs):
        with open(data_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                obj, created = AuthorAdvertisement.objects.get_or_create(
                    author_title=item['author_title'],
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created: {obj}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Object already exists: {obj}'))