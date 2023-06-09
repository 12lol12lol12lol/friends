
from friend_requests.models import FriendRequest
from friend_requests.services.common import is_already_friends
from user.constants import FriendshipStatus
from user.models import User

WRONG_FRIENDSHIP_REQUEST_MESSAGE = "You don't have friendship status with yourself"


class FriendshipStatusService:
    def __init__(self, from_user: User, to_user: User) -> None:
        self._from_user = from_user
        self._to_user = to_user

    def _is_incoming_request(self) -> bool:
        return FriendRequest.objects.filter(to_user=self._from_user, from_user=self._to_user).exists()

    def _is_outcoming_request(self) -> bool:
        return FriendRequest.objects.filter(to_user=self._to_user, from_user=self._from_user).exists()

    def run(self) -> tuple[bool, str, FriendshipStatus]:
        if self._from_user == self._to_user:
            return False, WRONG_FRIENDSHIP_REQUEST_MESSAGE, None
        if is_already_friends(self._from_user, self._to_user):
            return True, '', FriendshipStatus.already_friends
        if self._is_incoming_request():
            return True, '', FriendshipStatus.incoming_request
        if self._is_outcoming_request():
            return True, '', FriendshipStatus.outcoming_request
        return True, '', FriendshipStatus.nothing
