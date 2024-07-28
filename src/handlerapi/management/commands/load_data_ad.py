import json
import os

from django.core.management.base import BaseCommand

from handlerapi.models import Advertisement, AuthorAdvertisement

from config.settings import BASE_DIR


data_file_path = os.path.join(BASE_DIR, 'fixtures/data_ad.json')


class Command(BaseCommand):
    help = 'Load data from JSON file into the database'

    def handle(self, *args, **kwargs):
        with open(data_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                author_instance = AuthorAdvertisement.objects.filter(id=item['ad_author']).first()
                if not author_instance:
                    self.stdout.write(
                        self.style.ERROR(f'Author with ID {item["ad_author"]} does not exist. Skipping...'))
                    continue
                obj, created = Advertisement.objects.get_or_create(
                    ad_title=item['ad_title'],
                    ad_id=item['ad_id'],
                    ad_author=author_instance,
                    ad_views=item['ad_views'],
                    ad_position=item['ad_position']
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created: {obj}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Object already exists: {obj}'))
