from bson import json_util
from django.http import HttpResponse
import json
import jwt
import datetime
from django.conf import settings

from constants import PER_PAGE


def response_success(message = '', data = None, status_code = 200):
    if data is None:
        data = {}

    return HttpResponse(json.dumps({
        'status': 'Success',
        'status_code': status_code,
        'message': message,
        'data': data
    }), content_type = 'application/json', status = status_code)


def response_error(message = '', status_code = 400, error = None):
    if error is None:
        error = {}

    return HttpResponse(json.dumps({
        'status': 'Failed',
        'status_code': status_code,
        'message': message,
        'error': error
    }), content_type = 'application/json', status = status_code)


def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days = 7)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm = 'HS256')

    return token


def serialize_model_instance(instance, exclude):
    data = {}
    json_instance = json.loads(json_util.dumps(instance))
    _id = json_instance['_id']['$oid']

    for field in instance._meta.fields:
        field_name = field.name
        if field_name in exclude:
            continue
        if field_name == '_id':
            data['_id'] = _id
            continue
        field_value = getattr(instance, field_name)
        data[field_name] = field_value

    return data


def handle_query(request):
    q = request.GET.get('q')
    page_query = request.GET.get('page')
    sort_order = request.GET.get('sort_order')
    field = request.GET.get('field')
    category_id = request.GET.get('category_id')
    pk = request.GET.get('id')

    if sort_order and field:
        field = '-' + field if sort_order == 'desc' else field
    else:
        field = '-created_at'

    page = int(page_query) if page_query is not None else 1
    from_page = PER_PAGE * (page - 1)
    to_page = PER_PAGE

    return {
        'q': q,
        'sort_order': sort_order,
        'field': field,
        'from_page': from_page,
        'to_page': to_page,
        'page': page,
        'category_id': category_id,
        'pk': pk
    }
