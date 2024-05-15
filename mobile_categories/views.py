from rest_framework.decorators import api_view

from mobile_categories.models import Category
from mobile_categories.serializers import CategorySerializer
from helpers import response_success


# Create your views here.

@api_view(['GET'])
def get_all_categories(request):
    categories = Category.objects.filter(deleted = 0)
    response_data = {
        'categories': CategorySerializer(categories, many = True).data
    }
    return response_success('Success', response_data)
