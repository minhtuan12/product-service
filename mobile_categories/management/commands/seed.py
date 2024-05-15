from django.core.management.base import BaseCommand
from mobile_categories.models import Category


class Command(BaseCommand):
    help = 'Seeds the database.'

    def handle(self, *args, **options):
        Category.objects.all().delete()
        categories = [
            {
                'name': 'Samsung',
                'description': 'Samsung'
            },
            {
                'name': 'Apple',
                'description': 'Apple'
            },
            {
                'name': 'Huawei',
                'description': 'Huawei'
            },
            {
                'name': 'Xiaomi',
                'description': 'Xiaomi'
            },
            {
                'name': 'Oppo',
                'description': 'Oppo'
            }
        ]

        for category in categories:
            Category.objects.create(name = category['name'], description = category['description'])

        self.stdout.write(self.style.SUCCESS('Successfully seeded categories'))
