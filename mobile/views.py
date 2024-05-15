import json
import re
from bson import ObjectId
from django.db.models import Q
from rest_framework.decorators import api_view

from constants import PER_PAGE
from product.decorators import verify_token, check_permission
from mobile_categories.models import Category
from helpers import response_success, handle_query, response_error
from mobile.models import Mobile, MOBILE_STATUS
from mobile.requests import create_and_update_schema
from mobile.serializers import MobileSerializer
from mobile.validator import MobileValidator
from rest_framework import status as http_status
from ast import literal_eval


# Create your views here.

@api_view(['GET'])
def mobiles(request):
    queries = handle_query(request)

    if queries['category_id'] is not None:
        category_ids = queries['category_id'].split(',')
        for item in category_ids:
            if not ObjectId.is_valid(item):
                return response_error('Category ID must be an ObjectId.')

        exist_category = Category.objects.filter(_id__in = [ObjectId(item) for item in category_ids], deleted = 0)
        if not exist_category:
            return response_error('Category does not exist.')

    mobile_list = (Mobile.objects
                   .filter(deleted = 0, status = MOBILE_STATUS['AVAILABLE'])
                   .order_by(queries['field']))

    if queries['q'] is not None:
        mobile_list = mobile_list.filter(
            Q(name__icontains = queries['q'].strip()) |
            Q(code__icontains = queries['q'].strip())
        )

    if queries['pk'] is not None and ObjectId.is_valid(queries['pk']):
        mobile_list = mobile_list.filter(Q(pk = ObjectId(queries['pk'].strip())))

    if queries['category_id'] is not None:
        category_ids = queries['category_id'].split(',')
        category_object_ids = [ObjectId(item) for item in category_ids]
        mobile_list = mobile_list.filter(categories___id__in = category_object_ids)

    mobile_list = mobile_list[queries['from_page']:queries['to_page']]

    response_data = {
        'page': queries['page'],
        'per_page': PER_PAGE,
        'total': len(mobile_list),
        'mobiles': MobileSerializer(mobile_list, many = True).data
    }

    return response_success('Success', response_data)


@verify_token
@check_permission
@api_view(['GET'])
def admin_get_mobile(request):
    queries = handle_query(request)
    mobile_list = Mobile.objects.filter(deleted = 0).order_by(queries['field'])

    if queries['q'] is not None:
        q = queries['q'].strip()
        mobile_list = mobile_list.filter(Q(name__icontains = q) | Q(code__icontains = q))

    mobile_list = mobile_list[queries['from_page']:queries['to_page']]

    response_data = {
        'page': queries['page'],
        'per_page': PER_PAGE,
        'total': len(mobile_list),
        'mobiles': MobileSerializer(mobile_list, many = True).data
    }

    return response_success('Success', response_data)


@verify_token
@check_permission
@api_view(['POST'])
def create(request):
    (name, description, price,
     old_price, status, quantity, category_ids, image) = prepare_request(request)

    mobile = {
        'code': create_new_code(),
        'name': name,
        'description': description,
        'price': int(price),
        'old_price': int(old_price) if (old_price is not None and old_price.isnumeric()) else None,
        'status': int(status),
        'quantity': int(quantity),
        'image': image,
    }

    validator = MobileValidator(create_and_update_schema)
    if validator.validate(mobile):
        try:
            new_mobile = Mobile.objects.create(**mobile)
            category_ids = [ObjectId(category_id) for category_id in literal_eval(category_ids)]
            categories = Category.objects.filter(_id__in = category_ids, deleted = 0)
            new_mobile.categories.set(categories)

            return response_success('Created successfully')
        except Exception as e:
            return response_error('Error', http_status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response_error('Error', http_status.HTTP_400_BAD_REQUEST, validator.errors)


@verify_token
@check_permission
@api_view(['PUT'])
def update(request, id):
    # validate
    if not ObjectId.is_valid(id):
        return response_error('Mobile ID must be an ObjectId.', http_status.HTTP_400_BAD_REQUEST)

    mobile = Mobile.objects.filter(_id = ObjectId(id), deleted = 0)
    if not mobile:
        return response_error('Mobile does not exist.', http_status.HTTP_400_BAD_REQUEST)

    mobile = mobile[0]
    (name, description, price,
     old_price, status, quantity, category_ids, image) = prepare_request(request)

    update_mobile = {
        'code': mobile.code,
        'name': name,
        'description': description,
        'price': int(price),
        'old_price': int(old_price) if (old_price is not None and old_price.isnumeric()) else None,
        'status': int(status),
        'quantity': int(quantity),
        'image': image,
    }

    validator = MobileValidator(create_and_update_schema)
    if validator.validate(update_mobile):
        try:
            mobile.name = update_mobile['name']
            mobile.description = update_mobile['description']
            mobile.price = update_mobile['price']
            mobile.old_price = update_mobile['old_price']
            mobile.status = update_mobile['status']
            mobile.quantity = update_mobile['quantity']
            if image:
                mobile.image = update_mobile['image']
            mobile.save()

            category_ids = [ObjectId(category_id) for category_id in literal_eval(category_ids)]
            categories = Category.objects.filter(_id__in = category_ids, deleted = 0)
            mobile.categories.set(categories)

            return response_success('Updated successfully')
        except Exception as e:
            return response_error('Error', http_status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response_error('Error', http_status.HTTP_400_BAD_REQUEST, validator.errors)


@verify_token
@check_permission
@api_view(['DELETE'])
def delete(request, id):
    # validate
    if not ObjectId.is_valid(id):
        return response_error('Mobile ID must be an ObjectId.', http_status.HTTP_400_BAD_REQUEST)

    mobile = Mobile.objects.filter(_id = ObjectId(id), deleted = 0)
    if not mobile:
        return response_error('Mobile does not exist.', http_status.HTTP_400_BAD_REQUEST)

    mobile = mobile[0]
    mobile.deleted = 1
    mobile.save()
    mobile.categories.clear()

    return response_success('Deleted Successfully')


def create_new_code():
    latest_mobile = Mobile.objects.all().order_by('-created_at').first()
    latest_code_number = int(re.findall(r'\d+', latest_mobile.code)[0]) if latest_mobile is not None else -1
    return 'MB' + str(latest_code_number + 1)


def prepare_request(request):
    req = request.POST

    return [
        req.get("name"),
        req.get("description"),
        req.get("price"),
        req.get("old_price"),
        req.get("status"),
        req.get("quantity"),
        req.get("category_ids"),
        request.FILES.get("image")
    ]
