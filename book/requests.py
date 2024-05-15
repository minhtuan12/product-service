from constants import MAX_STRING_LENGTH
from book.models import BOOK_STATUS

create_and_update_schema = {
    'code': {},
    'title': {
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
    'author': {
        'type': 'string',
        'required': True,
        'maxlength': MAX_STRING_LENGTH
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
        'allowed': BOOK_STATUS.values()
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
    'deleted': {}
}
