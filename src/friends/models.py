from django.db import models
from django.contrib.auth.models import User
from friends.constants import FriendRequestStatus


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    to_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=64, choices=FriendRequestStatus)

    class Meta:
        ordering = ('-created_at', )
