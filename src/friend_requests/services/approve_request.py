

from friend_requests.constants import FriendRequestStatus
from friend_requests.models import FriendRequest
from friend_requests.services.common import add_to_friends, approve_requst
from friend_requests.services.constants import ALREADY_APPROVED_MESSAGE, SUCCESS_APPROVED_MESSAGE, WRONG_REQUEST_STATUS_MESSAGE


class ApproveRequestService:
    def __init__(self, request: FriendRequest) -> None:
        self._request = request

    def run(self) -> tuple[bool, str, FriendRequest | None]:
        if self._request.status in {FriendRequestStatus.approved, FriendRequestStatus.auto_approved}:
            return False, ALREADY_APPROVED_MESSAGE, None
        if self._request.status != FriendRequestStatus.new:
            return False, WRONG_REQUEST_STATUS_MESSAGE, None
        # Approve
        approve_requst(self._request)
        # Make friends
        add_to_friends(self._request.from_user, self._request.to_user)
        return True, SUCCESS_APPROVED_MESSAGE, self._request
