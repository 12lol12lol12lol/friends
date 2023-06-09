from exceptions.api_exceptions import BaseAPIException


class UserAPIException(BaseAPIException):
    default_detail = 'Error during user operation'
