from exceptions import BaseAPIException


class FriendRequestAPIException(BaseAPIException):
    default_detail = 'Error during requests operation'
