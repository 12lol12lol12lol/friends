from rest_framework.exceptions import APIException
from rest_framework import status


class BaseAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Any error.'

    def __init__(self, detail=None, code=None):
        code = self.status_code if code is None else code
        detail = self.default_detail if detail is None else detail
        super().__init__(detail, code)
