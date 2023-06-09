from friend_requests.constants import FriendRequestStatus
from friend_requests.models import FriendRequest
from friend_requests.services.common import decline_request, delete_from_friends
from friend_requests.services.constants import (
    ALREADY_APPROVED_MESSAGE, REQUEST_DECLINED_MESSAGE, WRONG_REQUEST_STATUS_MESSAGE,
)


class DeclineRequestService:
    def __init__(self, request: FriendRequest) -> None:
        self._request = request

    def run(self) -> tuple[bool, str, FriendRequest | None]:
        if self._request.status in {FriendRequestStatus.approved, FriendRequestStatus.auto_approved}:
            return False, ALREADY_APPROVED_MESSAGE, None
        if self._request.status != FriendRequestStatus.new:
            return False, WRONG_REQUEST_STATUS_MESSAGE, None
        # Decline
        request = decline_request(self._request)
        return True, REQUEST_DECLINED_MESSAGE, request
