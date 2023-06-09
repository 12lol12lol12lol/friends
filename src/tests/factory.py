from typing import Any
from friend_requests.constants import FriendRequestStatus
from friend_requests.models import FriendRequest
from tests.utils import get_test_user_password, get_test_username
from user.models import User


class TestFactory:

    def create_user(self, username: str = None, password: str = None) -> User:
        username = get_test_username() if username is None else username
        password = get_test_user_password() if password is None else password
        return User.objects.create_user(username=username, password=password)
    
    def create_request(
            self, from_user: User | None = None,
            to_user: User | None = None,
            status: FriendRequestStatus = FriendRequestStatus.new,
            message: str = '',
    ) -> FriendRequest:
        from_user = self.create_user() if from_user is None else from_user
        to_user = self.create_user() if to_user is None else to_user
        return FriendRequest.objects.create(
            from_user=from_user,
            to_user=to_user,
            status=status,
            message=message
        )
