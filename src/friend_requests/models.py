from django.db import models
from user.models import User
from friend_requests.constants import FriendRequestStatus


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+', db_index=True)
    to_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=64, choices=FriendRequestStatus.choices)
    message = models.CharField(max_length=1024, null=True, default=None)

    class Meta:
        ordering = ('-created_at', )
        unique_together = ('from_user', 'to_user')
