from django.db import transaction

from friend_requests.constants import FriendRequestStatus
from friend_requests.models import FriendRequest
from friend_requests.services.common import (
    add_to_friends, auto_approve_request, is_already_friends, is_already_request, is_already_sent, is_declined_request,
)
from friend_requests.services.constants import ALREADY_FRIENDS_MESSAGE, ALREADY_SENT_MESSAGE, AUTO_APPROVED_MESSAGE, DECLINED_MESSAGE, NEW_REQUEST_CREATED_MESSAGE, REQUEST_TO_YOURSELF_MESSAGE
from user.models import User


class SendRequestService:
    def __init__(self, from_user: User, to_user: User) -> None:
        self._from_user = from_user
        self._to_user = to_user

    @transaction.atomic
    def _create_auto_request(self) -> FriendRequest:
        friend_request = FriendRequest.objects.create(
            from_user=self._from_user,
            to_user=self._to_user,
            status=FriendRequestStatus.auto_approved,
            message=AUTO_APPROVED_MESSAGE,
        )
        add_to_friends(self._from_user, self._to_user)
        return friend_request

    def _create_new_request(self) -> FriendRequest:
        return FriendRequest.objects.create(
            from_user=self._from_user,
            to_user=self._to_user,
            status=FriendRequestStatus.new,
        )

    def run(self) -> tuple[bool, str, FriendRequest | None]:
        if self._from_user == self._to_user:
            return False, REQUEST_TO_YOURSELF_MESSAGE, None
        if is_already_friends(self._from_user, self._to_user):
            return False, ALREADY_FRIENDS_MESSAGE, None
        if is_already_sent(self._from_user, self._to_user):
            return False, ALREADY_SENT_MESSAGE, None
        if is_declined_request(from_user=self._from_user, to_user=self._to_user):
            return False, DECLINED_MESSAGE, None
        if (friend_request := is_already_request(self._from_user, self._to_user)):
            auto_requst = self._create_auto_request()
            auto_approve_request(friend_request)
            return True, AUTO_APPROVED_MESSAGE, auto_requst
        request = self._create_new_request()
        return True, NEW_REQUEST_CREATED_MESSAGE, request
