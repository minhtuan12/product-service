from functools import wraps

import jwt
import requests
from rest_framework import status

from constants import USER_ROLE
from helpers import response_error
from django.conf import settings


def verify_token(f):
    @wraps(f)
    def decorated(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', '')
        if not token:
            return response_error('Unauthorized', status.HTTP_401_UNAUTHORIZED)

        try:
            url = settings.USER_SERVICE_API_URL
            header = {
                "Content-Type": "application/json",
                "Authorization": token
            }

            result = requests.get(url, headers = header)
            if result.status_code == 200:
                current_user = result.json()['data']['user']
                request.user_role = current_user['role']

        except jwt.ExpiredSignatureError:
            return response_error('Token has expired', status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return response_error('Invalid token', status.HTTP_401_UNAUTHORIZED)
        except:
            return response_error('Unauthorized', status.HTTP_401_UNAUTHORIZED)

        return f(request, *args, **kwargs)

    return decorated


def check_permission(f):
    @wraps(f)
    def decorated(request, *args, **kwargs):
        try:
            if (not request.user_role) or (hasattr(request, 'user_role') and (request.user_role != USER_ROLE['ADMIN']
                                                                              and request.user_role != USER_ROLE[
                                                                                  'SUPER_ADMIN'])):
                return response_error('Forbidden', status.HTTP_403_FORBIDDEN)

            return f(request, *args, **kwargs)
        except:
            return response_error('Unauthorized', status.HTTP_401_UNAUTHORIZED)

    return decorated
