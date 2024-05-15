from django.core.management.base import BaseCommand
from clothes_categories.models import Category


class Command(BaseCommand):
    help = 'Seeds the database.'

    def handle(self, *args, **options):
        Category.objects.all().delete()
        categories = [
            {
                'name': 'Quần áo nam',
                'description': 'Quần áo dành cho nam'
            },
            {
                'name': 'Quần áo nữ',
                'description': 'Quần áo dành cho nữ'
            },
            {
                'name': 'Áo sơ mi',
                'description': 'Áo sơ mi'
            },
            {
                'name': 'Áo thun',
                'description': 'Áo thun'
            },
            {
                'name': 'Quần Jeans',
                'description': 'Quần Jeans'
            },
            {
                'name': 'Áo Khoác',
                'description': 'Áo Khoác'
            },
            {
                'name': 'Áo Vest và Comple',
                'description': 'Áo Vest và Comple'
            },
            {
                'name': 'Áo Cardigan',
                'description': 'Áo Cardigan'
            },
            {
                'name': 'Quần Shorts và Skirts',
                'description': 'Quần Shorts và Skirts'
            },
            {
                'name': 'Đồ Lót và Đồ Ngủ',
                'description': 'Đồ Lót và Đồ Ngủ'
            },
            {
                'name': 'Phụ kiện',
                'description': 'Phụ kiện'
            }
        ]

        for category in categories:
            Category.objects.create(name = category['name'], description = category['description'])

        self.stdout.write(self.style.SUCCESS('Successfully seeded categories'))
