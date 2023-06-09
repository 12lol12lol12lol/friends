from django.db import models


class FriendshipStatus(models.TextChoices):
    """
    (нет ничего / есть исходящая заявка / есть входящая заявка / уже друзья)
    """
    nothing = 'nothing'
    outcoming_request = 'outcoming_request'
    incoming_request = 'incoming_request'
    already_friends = 'already_friends'
