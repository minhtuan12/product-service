from rest_framework import serializers

from clothes_categories.serializers import CategorySerializer
from clothes.models import Clothes


class ClothesSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Clothes
        exclude = ['deleted']

    def get_categories(self, obj):
        categories = obj.categories.all()
        return CategorySerializer(categories, many = True).data
