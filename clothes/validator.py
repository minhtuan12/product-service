import mimetypes
from cerberus import Validator
from bson import ObjectId


class ClothesValidator(Validator):
    def _validate_is_greater_than(self, other_field, field, value):
        other_value = self.document[other_field]
        if other_value is not None and value is not None and not value > other_value:
            self._error(field, f"{field} must be bigger than {other_field}.")

    def _validate_type_objectid(self, value):
        if not isinstance(value, ObjectId):
            try:
                ObjectId(str(value))
                return True
            except (TypeError, ValueError):
                return self._error("Categories must be object id.")
        return True

    def _validate_is_image(self, is_image, field, value):
        if is_image and field and value:
            mime_type, _ = mimetypes.guess_type(value.name)
            if mime_type is None or not mime_type.startswith('image/'):
                self._error(field, "Must be an image")
