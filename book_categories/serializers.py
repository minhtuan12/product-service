from rest_framework import serializers
from book_categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['deleted', 'updated_at', 'created_at']
