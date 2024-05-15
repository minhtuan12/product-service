from django.core.management.base import BaseCommand
from book_categories.models import Category


class Command(BaseCommand):
    help = 'Seeds the database.'

    def handle(self, *args, **options):
        Category.objects.all().delete()
        categories = [
            {
                'name': 'Thriller',
                'description': 'thriller'
            },
            {
                'name': 'Comedy',
                'description': 'Comedy'
            },
            {
                'name': 'Action',
                'description': 'Action'
            },
            {
                'name': 'Non-action',
                'description': 'Non-action'
            }
        ]

        for category in categories:
            Category.objects.create(name = category['name'], description = category['description'])

        self.stdout.write(self.style.SUCCESS('Successfully seeded categories'))
