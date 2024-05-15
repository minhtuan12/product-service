from constants import MAX_STRING_LENGTH
from clothes.models import CLOTHES_STATUS

create_and_update_schema = {
    'code': {},
    'name': {
        'type': 'string',
        'required': True,
        'minlength': 1,
        'maxlength': MAX_STRING_LENGTH
    },
    'description': {
        'type': 'string',
        'maxlength': MAX_STRING_LENGTH,
        'nullable': True
    },
    'old_price': {
        'nullable': True,
        'type': 'integer',
        'min': 1,
        'is_greater_than': 'price'
    },
    'price': {
        'type': 'integer',
        'required': True,
        'min': 1,
    },
    'status': {
        'type': 'integer',
        'required': True,
        'allowed': CLOTHES_STATUS.values()
    },
    'quantity': {
        'type': 'integer',
        'required': True,
        'min': 1
    },
    'category_ids': {
        'type': 'list',
        'schema': {
            'type': 'objectid'
        }
    },
    'image': {
        'nullable': True,
        'is_image': True
    },
    'deleted_at': {}
}
