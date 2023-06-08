from enum import Enum


class FriendRequestStatus(Enum):
    new = 'new'
    declined = 'declined'
    approved = 'approved'
    delete = 'delete'
