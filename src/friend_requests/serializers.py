from rest_framework import serializers
from user.models import User
from friend_requests.models import FriendRequest


class CreateFriendRequestSerializer(serializers.Serializer):
    to_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('id', 'from_user', 'to_user', 'status')
