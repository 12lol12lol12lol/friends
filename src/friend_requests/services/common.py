from django.db import transaction

from friend_requests.constants import FriendRequestStatus
from friend_requests.models import FriendRequest
from friend_requests.services.constants import REQUEST_AUTO_APPROVED_MESSAGE
from user.models import User


def is_already_request(from_user: User, to_user: User) -> FriendRequestStatus:
    return FriendRequest.objects.filter(
        from_user=to_user, to_user=from_user,
        status__in={FriendRequestStatus.new, FriendRequestStatus.approved},
    ).first()

def is_already_exist(from_user: User, to_user: User) -> bool:
    return FriendRequest.objects.filter(
        from_user=from_user,
        to_user=to_user,
        status__in={FriendRequestStatus.new, FriendRequestStatus.approved}
    ).exists()

def is_declined_request(from_user: User, to_user: User) -> bool:
    return FriendRequest.objects.filter(
        from_user=from_user, to_user=to_user,
        status__in={FriendRequestStatus.declined, FriendRequestStatus.delete}
    ).exists()

def is_already_friends(from_user: User, to_user: User) -> bool:
    return from_user.friends.filter(id=to_user.id).exists()


@transaction.atomic
def add_to_friends(from_user: User, to_user: User) -> None:
    from_user.friends.add(to_user)
    to_user.friends.add(from_user)

@transaction.atomic
def delete_from_friends(from_user: User, to_user: User) -> None:
    from_user.friends.remove(to_user)
    to_user.friends.remove(from_user)

def auto_approve_request(request: FriendRequest) -> None:
    request.status = FriendRequestStatus.auto_approved
    request.message = REQUEST_AUTO_APPROVED_MESSAGE
    request.save()

def approve_requst(request: FriendRequest) -> FriendRequest:
    request.status = FriendRequestStatus.approved
    request.save()
    return request

def decline_request(request: FriendRequest) -> None:
    request.status = FriendRequestStatus.declined
    request.save()
    return request

def is_already_sent(from_user: User, to_user: User) -> bool:
    return FriendRequest.objects.filter(
        from_user=from_user,
        to_user=to_user,
        status=FriendRequestStatus.new
    ).exists()

def make_delete_request(from_user: User, to_user: User) -> FriendRequest:
    request = None
    try:
        request = FriendRequest.objects.get(from_user=from_user, to_user=to_user)
    except FriendRequest.DoesNotExist:
        request = FriendRequest.objects.create(
            from_user=from_user,
            to_user=to_user,
            status=FriendRequestStatus.delete,
        )
    request.status = FriendRequestStatus.delete
    request.message = f'User {from_user.id} delete user {to_user.id} from friends'
    request.save()
    return request
