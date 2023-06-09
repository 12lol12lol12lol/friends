from django.db import models


class FriendRequestStatus(models.TextChoices):
    new = 'new'
    declined = 'declined'
    approved = 'approved'
    delete = 'delete'
    auto_delete = 'auto_delete'
    auto_approved = 'auto_approved'
