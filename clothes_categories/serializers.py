from rest_framework import serializers
from clothes_categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['deleted', 'created_at', 'updated_at']
