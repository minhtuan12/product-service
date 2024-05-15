from rest_framework import serializers

from book_categories.serializers import CategorySerializer
from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Book
        exclude = ['deleted']

    def get_categories(self, obj):
        categories = obj.categories.all()
        return CategorySerializer(categories, many = True).data
