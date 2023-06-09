
from friend_requests.services.common import make_delete_request, delete_from_friends, is_already_friends
from user.models import User

YOU_ARE_NOT_FRIENDS_MESSAGE = 'You are not friends'
DELETE_YOURSELF_FROM_FRIENDS_MESSAGE = 'Wrong operation. You try to delete yourself from friends'


class DeleteFromFriendsService:
    def __init__(self, from_user: User, to_user: User) -> None:
        self._from_user = from_user
        self._to_user = to_user


    def run(self) -> tuple[bool, str, None]:
        if self._from_user == self._to_user:
            return False, DELETE_YOURSELF_FROM_FRIENDS_MESSAGE, None
        if not is_already_friends(self._from_user, self._to_user):
            return False, YOU_ARE_NOT_FRIENDS_MESSAGE, None
        delete_from_friends(self._from_user, self._to_user)
        make_delete_request(self._to_user, self._from_user)
        return True,'', None